"""Offline-only regression tests for the prospective Catholic pilot trace contract.

All prompts, answers and calls below are invented fixtures. No external
providers or participants are contacted, and no research run is authorized.
"""
from __future__ import annotations

import importlib.util
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "catholic-ai-pilot/_tools/prompt_trace.py"
spec = importlib.util.spec_from_file_location("catholic_trace_fixture", MODULE)
trace = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trace)
POLICY = ROOT / "catholic-ai-pilot/_evidence/trace-policy/next-run-gate.json"


def create_fixture(root: Path, *, max_attempts: int = 3) -> None:
    plan = b'{"case":"SYNTHETIC ONLY","model_calls":0}\n'
    (root / "plan.json").write_bytes(plan)
    manifest = {
        "schema": trace.VERSION,
        "run_id": "SYNTHETIC-TRACE-TEST",
        "run_kind": "offline_fixture",
        "fixture_disclosure": "synthetic_unit_test_only_no_research_calls",
        "capture_scope": "exact_caller_visible_payloads",
        "source_data_classification": "synthetic_or_public_rights_cleared",
        "frozen_plan": {
            "relative_path": "plan.json",
            "sha256": hashlib.sha256(plan).hexdigest(),
            "freeze_commit": None,
        },
        "allowed_tools": ["offline.fake"],
        "max_attempts": max_attempts,
        "approvals": {},
    }
    (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")


def provider_info() -> dict:
    return {
        "provider": "offline.synthetic.unit.test",
        "model_id": None,
        "model_id_state": "not_exposed",
        "model_id_unavailable_reason": "No actual provider exists in fixture.",
        "generation_parameters": None,
        "generation_parameters_state": "not_exposed",
        "parameters_unavailable_reason": "No actual provider exists in fixture.",
        "transport_bytes_state": "not_captured",
    }


def call(
    root: Path,
    *,
    call_id="fake-1",
    case_id="fixture-001",
    attempt=1,
    prompt="SYNTHETIC: explain an invented parish event.\nKeep the citation separate.",
    invoke=None,
    extractor=None,
    provenance=None,
    max_fixture=True,
):
    if invoke is None:
        invoke = lambda args: {"answer": "SYNTHETIC ONLY.\nNo Church judgment.", "refs": []}
    if extractor is None:
        extractor = lambda value: value.get("answer")
    return trace.record_call(
        root, call_id=call_id, case_id=case_id, attempt=attempt,
        kind="model", tool_name="offline.fake", prompt_text=prompt,
        visible_args={"prompt": prompt}, provenance=provenance or provider_info(),
        invoke=invoke, response_text_from=extractor, offline_fixture=max_fixture,
    )


class TraceRecorderFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        create_fixture(self.root)

    def events(self):
        return [json.loads(line) for line in (self.root / "events.jsonl").read_text().splitlines()]

    def test_success_preserves_verbatim_prompt_and_visible_payload(self):
        question = "SYNTHETIC café\n«é» \u00e1"
        answer = "SYNTHETIC response\nGreek \u03b1"
        called = []
        def provider(args):
            called.append(args)
            return {"answer": answer, "references": [{"title": "Invented synthetic"}]}
        out = call(self.root, prompt=question, invoke=provider)
        self.assertEqual(out["answer"], answer)
        self.assertEqual(called, [{"prompt": question}])
        row = self.events()
        self.assertEqual(len(row), 2)
        self.assertEqual(row[0]["prompt_text"], question)
        self.assertEqual(row[0]["visible_args"], {"prompt": question})
        self.assertEqual(row[1]["response_text"], answer)
        self.assertEqual(row[1]["visible_result"], out)
        self.assertEqual(row[0]["prompt_sha256"], hashlib.sha256(question.encode()).hexdigest())
        self.assertEqual(row[1]["response_sha256"], hashlib.sha256(answer.encode()).hexdigest())
        report = trace.verify_run(self.root)
        self.assertEqual(report["successes"], 1)
        self.assertFalse(report["research_validity_established"])

    def test_failure_retained_and_retry_has_separate_attempt_id(self):
        def failed(_args):
            raise RuntimeError("INVENTED_SECRET_STRING: do not disclose")
        with self.assertRaises(RuntimeError):
            call(self.root, call_id="fake-error", invoke=failed)
        call(self.root, call_id="fake-retry", attempt=2)
        ev = self.events()
        self.assertEqual([x["event"] for x in ev], ["start", "error", "start", "success"])
        self.assertNotIn("INVENTED_SECRET_STRING", (self.root / "events.jsonl").read_text())
        rep = trace.verify_run(self.root)
        self.assertEqual((rep["unique_calls"], rep["errors"], rep["successes"]), (2, 1, 1))

    def test_wrong_attempt_number_blocks_before_external_function(self):
        called = []
        with self.assertRaises(trace.CaptureError):
            call(self.root, attempt=2, invoke=lambda a: called.append(a))
        self.assertEqual(called, [])
        self.assertFalse((self.root / "events.jsonl").exists())

    def test_repeated_call_id_blocks_before_duplicate_call(self):
        call(self.root, call_id="first")
        called = []
        with self.assertRaises(trace.CaptureError):
            call(self.root, call_id="first", attempt=2, invoke=lambda a: called.append(a))
        self.assertEqual(called, [])
        self.assertEqual(len(self.events()), 2)

    def test_budget_limits_total_attempts_including_errors(self):
        create_fixture(self.root, max_attempts=1)
        call(self.root, call_id="once")
        with self.assertRaises(trace.CaptureError):
            call(self.root, call_id="twice", attempt=2)
        self.assertEqual(len(self.events()), 2)

    def test_missing_answer_is_incomplete_and_cannot_be_promoted(self):
        with self.assertRaises(trace.CaptureError):
            call(self.root, invoke=lambda a: {"references": []})
        rep = trace.verify_run(self.root)
        self.assertEqual(rep["incomplete_captures"], 1)
        self.assertEqual(rep["open_requests"], 0)
        with self.assertRaises(trace.CaptureError):
            trace.promotion_gate(self.root)
        self.assertEqual(self.events()[-1]["event"], "incomplete_capture")

    def test_response_extractor_failure_closes_request_explicitly(self):
        with self.assertRaises(trace.CaptureError):
            call(self.root, invoke=lambda a: {"answer": "SYNTHETIC"}, extractor=lambda a: 7)
        self.assertEqual(trace.verify_run(self.root)["open_requests"], 0)
        self.assertEqual(self.events()[-1]["event"], "incomplete_capture")

    def test_hash_chain_detects_tampering(self):
        call(self.root)
        path = self.root / "events.jsonl"
        data = path.read_text()
        self.assertIn("fixture-001", data)
        path.write_text(data.replace("fixture-001", "fixture-999"))
        with self.assertRaises(trace.CaptureError):
            trace.verify_run(self.root)

    def test_started_but_unfinished_request_blocks_verification(self):
        call(self.root)
        path = self.root / "events.jsonl"
        lines = path.read_text().splitlines()
        path.write_text(lines[0] + "\n")
        with self.assertRaises(trace.CaptureError):
            trace.verify_run(self.root)
        self.assertEqual(trace.verify_run(self.root, require_closed=False)["open_requests"], 1)

    def test_secret_bearing_request_field_blocks_before_call(self):
        called = []
        with self.assertRaises(trace.CaptureError):
            trace.record_call(
                self.root, call_id="q1", case_id="fixture-001", attempt=1,
                kind="model", tool_name="offline.fake", prompt_text="Synthetic",
                visible_args={"prompt": "Synthetic", "api_key": "secret"},
                provenance=provider_info(), invoke=lambda args: called.append(args),
                response_text_from=lambda r: r.get("answer"), offline_fixture=True,
            )
        self.assertEqual(called, [])
        self.assertFalse((self.root / "events.jsonl").exists())

    def test_sensitive_result_is_withheld_and_run_marked_incomplete(self):
        with self.assertRaises(trace.CaptureError):
            call(self.root, invoke=lambda a: {"answer": "Invented", "access_token": "secret-content"})
        content = (self.root / "events.jsonl").read_text()
        self.assertNotIn("secret-content", content)
        self.assertEqual(trace.verify_run(self.root)["incomplete_captures"], 1)

    def test_non_serializable_result_fails_closed(self):
        with self.assertRaises(trace.CaptureError):
            call(self.root, invoke=lambda a: {"answer": set(["nonjson"])})
        self.assertEqual(trace.verify_run(self.root)["incomplete_captures"], 1)

    def test_unknown_provider_model_requires_disclosed_reason(self):
        info = provider_info()
        info["model_id_unavailable_reason"] = None
        with self.assertRaises(trace.CaptureError):
            call(self.root, provenance=info)
        self.assertFalse((self.root / "events.jsonl").exists())

    def test_pending_and_unapproved_confirmatory_manifest_blocks_call(self):
        policy = json.loads(POLICY.read_text())
        self.assertEqual(policy["policy_status"], "MANDATORY_FUTURE_GATE_NOT_YET_APPROVED")
        pending = policy["pending_run_manifest"]
        self.assertTrue(all(not item["approved"] for item in pending["approvals"].values()))
        pending["frozen_plan"]["sha256"] = hashlib.sha256((self.root / "plan.json").read_bytes()).hexdigest()
        (self.root / "manifest.json").write_text(json.dumps(pending))
        called = []
        with self.assertRaises(trace.CaptureError):
            call(self.root, invoke=lambda a: called.append(a), max_fixture=False)
        self.assertEqual(called, [])
        self.assertFalse((self.root / "events.jsonl").exists())

    def test_fixture_mode_cannot_pass_real_preflight_or_release(self):
        with self.assertRaises(trace.CaptureError):
            trace.validate_manifest(self.root)
        call(self.root)
        with self.assertRaises(trace.CaptureError):
            trace.promotion_gate(self.root)

    def test_plan_bytes_mutation_blocks_before_any_call(self):
        (self.root / "plan.json").write_text("changed")
        with self.assertRaises(trace.CaptureError):
            call(self.root)
        self.assertFalse((self.root / "events.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
