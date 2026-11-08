#!/usr/bin/env python3
"""Prospective caller-visible prompt/output capture contract for the Catholic pilot.

No network calls, model access, reviewers, or run approvals are supplied here.
For real runs, invoke only after a separately documented research-owner freeze.
Legacy experiments retain their original capture limitations and are not rewritten.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

VERSION = "node-norm-visible-trace-1"
APPROVALS = (
    "research_owner_decision",
    "protocol_and_cases_frozen",
    "source_rights",
    "privacy_and_ethics",
    "reviewer_independence_plan",
    "outcomes_budget_and_stopping",
)
KNOWN_KIND = {"model", "agent", "tool"}


class CaptureError(ValueError):
    """Record may not be executed or promoted as a complete trace."""


def canonical(value: Any) -> bytes:
    """Stable representation of a caller-visible JSON object, NOT HTTP raw bytes."""
    return json.dumps(
        value, sort_keys=True, ensure_ascii=False, allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _path_within(root: Path, name: str) -> Path:
    if not name or Path(name).is_absolute():
        raise CaptureError("Source plan must be a relative file within the run directory.")
    child = (root / name).resolve()
    if not child.is_relative_to(root.resolve()):
        raise CaptureError("Plan path leaves the run directory.")
    return child


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(run_dir: Path, *, offline_fixture: bool = False) -> dict:
    """Fail closed for prospective studies; a fixture exception is test-only."""
    run_dir = Path(run_dir)
    path = run_dir / "manifest.json"
    if not path.is_file():
        raise CaptureError("Missing run manifest; no external call permitted.")
    manifest = _read_json(path)
    if manifest.get("schema") != VERSION:
        raise CaptureError("Unknown capture schema.")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,90}", str(manifest.get("run_id", ""))):
        raise CaptureError("Invalid run identifier.")
    if manifest.get("capture_scope") != "exact_caller_visible_payloads":
        raise CaptureError("Must capture the exact caller-visible arguments and results.")
    if manifest.get("source_data_classification") != "synthetic_or_public_rights_cleared":
        raise CaptureError("Sensitive or unreviewed data cannot be committed to the public trace.")
    plan = manifest.get("frozen_plan", {})
    plan_path = _path_within(run_dir, plan.get("relative_path", ""))
    if not plan_path.is_file():
        raise CaptureError("The plan source file does not exist.")
    expected = plan.get("sha256")
    if not isinstance(expected, str) or sha256_bytes(plan_path.read_bytes()) != expected:
        raise CaptureError("Frozen plan SHA-256 mismatch or missing.")
    kind = manifest.get("run_kind")
    if kind == "offline_fixture" and offline_fixture:
        if manifest.get("fixture_disclosure") != "synthetic_unit_test_only_no_research_calls":
            raise CaptureError("Offline fixture is not marked as a nonresearch unit test.")
    elif kind == "confirmatory":
        commit = plan.get("freeze_commit")
        if not isinstance(commit, str) or not re.fullmatch("[a-f0-9]{40}", commit):
            raise CaptureError("Frozen Git commit has not been recorded.")
        approval = manifest.get("approvals", {})
        for name in APPROVALS:
            row = approval.get(name)
            if not isinstance(row, dict) or row.get("approved") is not True:
                raise CaptureError("Approval gate unresolved: " + name)
            if not all(isinstance(row.get(f), str) and row[f].strip()
                       for f in ("decision_url", "approver", "decision_timestamp")):
                raise CaptureError("Missing decision provenance: " + name)
    else:
        raise CaptureError("Only approved confirmatory runs can invoke external tools.")
    if not isinstance(manifest.get("allowed_tools"), list) or not manifest["allowed_tools"]:
        raise CaptureError("Tool allowlist must be fixed before a call.")
    if not isinstance(manifest.get("max_attempts"), int) or manifest["max_attempts"] < 1:
        raise CaptureError("Call budget must be a positive integer.")
    return manifest


def _read_events(fh) -> list[dict]:
    fh.seek(0)
    raw = fh.read()
    if not raw:
        return []
    if not raw.endswith("\n"):
        raise CaptureError("Incomplete event write detected; do not truncate history.")
    try:
        return [json.loads(line) for line in raw.splitlines()]
    except json.JSONDecodeError as error:
        raise CaptureError("Invalid or partly written JSONL event.") from error


def verify_events(events: list[dict], *, require_closed: bool = True) -> dict:
    """Verify record order, hash chain, starts, failures, and missing captures."""
    last = None
    active: dict[str, dict] = {}
    used: set[str] = set()
    case_attempts: dict[str, int] = {}
    completed = errors = incomplete = 0
    for i, ev in enumerate(events, 1):
        if ev.get("seq") != i or ev.get("previous_sha256") != last:
            raise CaptureError("Event sequence or previous-hash mismatch.")
        content = {k: v for k, v in ev.items() if k != "event_sha256"}
        check = sha256_bytes(canonical(content))
        if ev.get("event_sha256") != check:
            raise CaptureError("Event payload checksum mismatch.")
        last = check
        action = ev.get("event")
        call_id = ev.get("call_id")
        if not isinstance(call_id, str) or not call_id:
            raise CaptureError("Call ID must be nonempty.")
        if action == "start":
            if call_id in active or call_id in used:
                raise CaptureError("A retry or repeated call cannot overwrite its original ID.")
            case_id = ev.get("case_id")
            attempt = ev.get("attempt")
            if not isinstance(case_id, str) or not case_id:
                raise CaptureError("Missing case identifier.")
            if not isinstance(attempt, int) or attempt != case_attempts.get(case_id, 0) + 1:
                raise CaptureError("Case attempts must be numbered consecutively, including failures.")
            if ev.get("kind") not in KNOWN_KIND:
                raise CaptureError("Unknown call kind.")
            if "visible_args" not in ev:
                raise CaptureError("Full caller-visible arguments are missing.")
            if ev.get("kind") in {"model", "agent"}:
                if not isinstance(ev.get("prompt_text"), str) or not ev["prompt_text"]:
                    raise CaptureError("Model or agent prompt must be captured verbatim.")
            prompt = ev.get("prompt_text")
            if ev.get("prompt_sha256") != (sha256_bytes(prompt.encode("utf-8")) if prompt is not None else None):
                raise CaptureError("Prompt checksum does not match exact retained text.")
            if ev.get("visible_args_sha256") != sha256_bytes(canonical(ev["visible_args"])):
                raise CaptureError("Visible request checksum mismatch.")
            active[call_id] = ev
            used.add(call_id)
            case_attempts[case_id] = attempt
        elif action in {"success", "error", "incomplete_capture"}:
            if call_id not in active:
                raise CaptureError("An output or error has no preceding request record.")
            start = active.pop(call_id)
            if ev.get("run_id") != start.get("run_id"):
                raise CaptureError("Request/output run ID mismatch.")
            if action == "success":
                if "visible_result" not in ev or ev.get("visible_result_sha256") != sha256_bytes(canonical(ev["visible_result"])):
                    raise CaptureError("Full visible result or its checksum is missing.")
                response = ev.get("response_text")
                if ev.get("kind") in {"model", "agent"} and not isinstance(response, str):
                    raise CaptureError("Model response text is missing.")
                if ev.get("response_sha256") != (sha256_bytes(response.encode("utf-8")) if response is not None else None):
                    raise CaptureError("Response checksum does not match exact retained text.")
                completed += 1
            elif action == "error":
                if not ev.get("error_type") or ev.get("error_message_state") not in {
                    "sanitized", "not_retained_privacy"
                }:
                    raise CaptureError("Error reporting omissions must be declared.")
                errors += 1
            else:
                if not ev.get("reason") or "visible_result" not in ev:
                    raise CaptureError("Partial-result capture must explain its limitation.")
                incomplete += 1
        else:
            raise CaptureError("Unknown event type.")
    if require_closed and active:
        raise CaptureError("Started request lacks a terminal response/error: " + ",".join(active))
    return {
        "events": len(events), "successes": completed, "errors": errors,
        "incomplete_captures": incomplete, "open_requests": len(active),
        "last_sha256": last, "unique_calls": len(used),
        "research_validity_established": False,
    }


def _append(run_dir: Path, record: dict) -> dict:
    """Append-only JSONL under an advisory file lock, fsynced before returning."""
    path = run_dir / "events.jsonl"
    with open(path, "a+", encoding="utf-8") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        events = _read_events(fh)
        verify_events(events, require_closed=False)
        previous = events[-1]["event_sha256"] if events else None
        event = {
            "schema": VERSION, "seq": len(events) + 1,
            "previous_sha256": previous, "recorded_at_utc": utc_now(), **record,
        }
        event["event_sha256"] = sha256_bytes(canonical(event))
        # Validate the candidate under the same file lock before writing it.
        verify_events(events + [event], require_closed=False)
        fh.seek(0, os.SEEK_END)
        fh.write(json.dumps(event, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())
        fcntl.flock(fh, fcntl.LOCK_UN)
    return event


def verify_run(run_dir: Path, *, require_closed: bool = True) -> dict:
    """Read the existing trace. Checks integrity, not factual or theological validity."""
    path = Path(run_dir) / "events.jsonl"
    if not path.exists():
        raise CaptureError("Trace file not yet created.")
    with open(path, encoding="utf-8") as fh:
        events = _read_events(fh)
    report = verify_events(events, require_closed=require_closed)
    report["run_dir"] = str(Path(run_dir))
    return report


def promotion_gate(run_dir: Path) -> dict:
    """Block release when a confirmatory run has missing prompts or outputs."""
    manifest = validate_manifest(run_dir)
    report = verify_run(run_dir, require_closed=True)
    if report["incomplete_captures"]:
        raise CaptureError("An incomplete captured response blocks research release.")
    if not report["unique_calls"]:
        raise CaptureError("No tool/model calls were recorded.")
    if report["unique_calls"] > manifest["max_attempts"]:
        raise CaptureError("Recorded calls exceed the frozen attempt budget.")
    return {**report, "capture_gate": "passed_for_integrity_only", "independent_validation": False}


def _reject_secret_keys(value: Any) -> None:
    """Coarse public-log guard. Human privacy review remains mandatory."""
    if isinstance(value, dict):
        for key, item in value.items():
            if re.search(r"(^|_)(password|api_key|access_token|secret|authorization|cookie)(_|$)", str(key).lower()):
                raise CaptureError("Possible secret-bearing field: public trace blocked.")
            _reject_secret_keys(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _reject_secret_keys(item)


def record_call(
    run_dir: Path, *,
    call_id: str,
    case_id: str,
    attempt: int,
    kind: str,
    tool_name: str,
    prompt_text: str | None,
    visible_args: dict,
    provenance: dict,
    invoke: Callable[[dict], Any],
    response_text_from: Callable[[Any], str | None],
    offline_fixture: bool = False,
) -> Any:
    """Persist request BEFORE invoking caller-visible tool. Preserve success or failure.

    invoke receives precisely the serialized visible_args; external provider
    defaults/hidden retrieval cannot be claimed as observed.
    """
    run_dir = Path(run_dir)
    manifest = validate_manifest(run_dir, offline_fixture=offline_fixture)
    if tool_name not in manifest["allowed_tools"]:
        raise CaptureError("Tool not in frozen allowlist.")
    if kind not in KNOWN_KIND or not isinstance(visible_args, dict):
        raise CaptureError("Unsupported invocation structure.")
    if kind in {"model", "agent"} and (not isinstance(prompt_text, str) or not prompt_text):
        raise CaptureError("Missing model/agent prompt.")
    if isinstance(visible_args.get("prompt"), str) and visible_args["prompt"] != prompt_text:
        raise CaptureError("Prompt differs from the exact arguments passed to the tool.")
    if not isinstance(provenance, dict) or not provenance.get("provider"):
        raise CaptureError("Provider attribution must be recorded.")
    for val, state, reason in (
        ("model_id", "model_id_state", "model_id_unavailable_reason"),
        ("generation_parameters", "generation_parameters_state", "parameters_unavailable_reason"),
    ):
        if provenance.get(val) is None and (
            provenance.get(state) not in {"not_exposed", "not_applicable"}
            or not provenance.get(reason)
        ):
            raise CaptureError("Unknown model/configuration data needs an explicit reason.")
    if provenance.get("transport_bytes_state") != "not_captured":
        raise CaptureError("This wrapper does not capture original HTTP transport bytes.")
    # Never write known secret-bearing keys to public Git history.
    _reject_secret_keys(visible_args)
    visible_hash = sha256_bytes(canonical(visible_args))
    prompt_hash = sha256_bytes(prompt_text.encode("utf-8")) if prompt_text is not None else None
    path = run_dir / "events.jsonl"
    if path.exists():
        status = verify_run(run_dir, require_closed=True)
        if status["unique_calls"] >= manifest["max_attempts"]:
            raise CaptureError("Frozen call budget exhausted.")
    elif manifest["max_attempts"] < 1:
        raise CaptureError("No call budget.")
    start = {
        "event": "start", "run_id": manifest["run_id"], "call_id": call_id,
        "case_id": case_id, "attempt": attempt, "kind": kind,
        "tool_name": tool_name, "prompt_text": prompt_text,
        "prompt_sha256": prompt_hash, "visible_args": visible_args,
        "visible_args_sha256": visible_hash, "provider": provenance,
        "request_capture_scope": "exact_caller_visible_arguments",
    }
    # Verify the prospective event against existing events BEFORE making the call.
    existing = []
    if path.exists():
        with open(path, encoding="utf-8") as fh:
            existing = _read_events(fh)
    hypothetical = {
        "schema": VERSION, "seq": len(existing) + 1,
        "previous_sha256": existing[-1]["event_sha256"] if existing else None,
        "recorded_at_utc": utc_now(), **start,
    }
    hypothetical["event_sha256"] = sha256_bytes(canonical(hypothetical))
    verify_events(existing + [hypothetical], require_closed=False)
    _append(run_dir, start)
    try:
        result = invoke(visible_args)
    except Exception as exc:
        _append(run_dir, {
            "event": "error", "run_id": manifest["run_id"],
            "call_id": call_id, "kind": kind,
            "error_type": type(exc).__name__, "error_message_state": "not_retained_privacy",
            "error_text": None, "error_capture_limitation": "Exception text may contain sensitive data.",
        })
        raise
    try:
        _reject_secret_keys(result)
    except CaptureError:
        _append(run_dir, {
            "event": "incomplete_capture", "run_id": manifest["run_id"],
            "call_id": call_id, "kind": kind,
            "visible_result": {"withheld_from_public_log": True},
            "reason": "Response may contain secrets; secure private quarantine is required.",
            "response_text_state": "withheld_due_to_privacy",
        })
        raise
    try:
        result_hash = sha256_bytes(canonical(result))
        answer = response_text_from(result)
        if answer is not None and not isinstance(answer, str):
            raise CaptureError("Response extractor returned a non-text answer.")
    except Exception as exc:
        # Record the caller-visible result if JSON-safe; otherwise mark it
        # omitted explicitly. Never silently leave a request marked complete.
        try:
            canonical(result)
            safe_result = result
        except (TypeError, ValueError):
            safe_result = {"not_serializable": True}
        _append(run_dir, {
            "event": "incomplete_capture", "run_id": manifest["run_id"],
            "call_id": call_id, "kind": kind, "visible_result": safe_result,
            "reason": "Result serialization or answer extraction failed.",
            "response_text_state": "not_captured",
        })
        raise CaptureError("Result could not be fully captured.") from exc
    if kind in {"model", "agent"} and answer is None:
        _append(run_dir, {
            "event": "incomplete_capture", "run_id": manifest["run_id"],
            "call_id": call_id, "kind": kind, "visible_result": result,
            "reason": "Caller-visible model answer text was unavailable.",
            "response_text_state": "not_exposed",
        })
        raise CaptureError("Model output lacks a verbatim answer; preserve as incomplete.")
    _append(run_dir, {
        "event": "success", "run_id": manifest["run_id"], "call_id": call_id,
        "kind": kind, "visible_result": result,
        "visible_result_sha256": result_hash,
        "response_text": answer,
        "response_sha256": sha256_bytes(answer.encode("utf-8")) if answer is not None else None,
        "response_capture_scope": "caller_visible_payload_not_raw_http",
    })
    return result


def main() -> int:
    p = argparse.ArgumentParser(description="Offline preflight and trace verification; no service calls.")
    p.add_argument("action", choices=("preflight", "verify", "promote-check"))
    p.add_argument("run_dir", type=Path)
    p.add_argument("--allow-incomplete", action="store_true")
    args = p.parse_args()
    if args.action == "preflight":
        manifest = validate_manifest(args.run_dir)
        print(json.dumps({"run_id": manifest["run_id"], "preflight": "passed"}, indent=2))
    elif args.action == "verify":
        print(json.dumps(verify_run(args.run_dir, require_closed=not args.allow_incomplete), indent=2))
    else:
        print(json.dumps(promotion_gate(args.run_dir), indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CaptureError, OSError, ValueError) as exc:
        print("CAPTURE GATE BLOCKED:", str(exc))
        raise SystemExit(2)
