"""Explicit input identity and serialization; no repository-global state."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from typing import Any
from .capabilities import TeamBlocked

def canonical(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(obj: Any) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


def load_spec(path: Path, expected_sha256: str) -> dict:
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected_sha256:
        raise TeamBlocked('Specification bytes differ from the approved layout manifest.')
    value=json.loads(raw)
    if not isinstance(value,dict):
        raise TeamBlocked('Specification must be a JSON object.')
    return value
