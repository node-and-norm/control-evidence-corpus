"""CITATION-GATE-001: offline identity checks, never theological approval.

The locator diagnostic is a bounded adaptation of the existing derive() field
comparison. It is not the existing site's citation-admission policy. The simple
checklist and structured gate implement the same declared eligibility criteria.
All source content used in authored cases is explicitly synthetic.
"""
from __future__ import annotations
import hashlib
import re
import unicodedata
from urllib.parse import urlparse


def canonical_text(value: str) -> str:
    return ' '.join(unicodedata.normalize('NFC', value).split())


def digest(value: str) -> str:
    return hashlib.sha256(canonical_text(value).encode('utf-8')).hexdigest()


def paragraph(value: object) -> int | None:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        return None
    match = re.fullmatch(r'(?:para-)?(\d+)', str(value).strip())
    return int(match.group(1)) if match else None


def pointer(url: object) -> tuple[str, int] | None:
    if not isinstance(url, str):
        return None
    try:
        p = urlparse(url)
        if p.scheme != 'https' or p.hostname != 'www.magisterium.com':
            return None
        if p.username or p.password or p.port not in (None, 443):
            return None
        match = re.fullmatch(r'/docs/([a-zA-Z0-9-]+)/ref/((?:para-)?\d+)/?', p.path)
        if not match:
            return None
        return match.group(1), int(match.group(2).removeprefix('para-'))
    except ValueError:
        return None


def locator_diagnostic(case: dict) -> dict:
    """Legacy field-comparison diagnostic, not an admission rule."""
    selected, fetched = case['selected'], case['fetched']
    expected = selected.get('url', '').rstrip('/').split('/')[-1]
    actual = fetched.get('ref')
    status = 'fetch_not_found' if not fetched.get('found') else (
        'locator_match' if actual == expected else 'locator_mismatch')
    return {'status': status, 'positive_locator_signal': status == 'locator_match',
            'semantic_support': 'unreviewed', 'answer_verified': False}


def simple_checklist(case: dict, registry: dict) -> dict:
    """Short-circuit checklist: same facts and criteria as the structured gate."""
    s, f, t = case['selected'], case['fetched'], case['target']
    key = f"{t['document']}:{t['paragraph']}:{t['edition']}:{t['language']}"
    ref = registry.get(key)
    request_ok = f.get('requested_id') == s.get('id')
    found_ok = f.get('found') is True and f.get('returned_id') == s.get('id')
    a, b = pointer(s.get('url')), pointer(f.get('url'))
    pointer_ok = a == b == (t['document'], t['paragraph'])
    metadata_ok = (paragraph(f.get('ref')) == t['paragraph'] and
                   f.get('document') == t['document'])
    origin_ok = bool(ref and ref.get('locator_observed') is True)
    edition_ok = f.get('edition') == t['edition'] and f.get('language') == t['language']
    related = [x for x in case['search_results'] if x.get('id') == s.get('id')]
    bindings = {pointer(x.get('url')) for x in related}
    binding_ok = bool(related) and bindings == {(t['document'], t['paragraph'])}
    body_ok = (isinstance(f.get('body'), str) and bool(f['body'].strip()) and
               bool(ref) and digest(f['body']) == ref.get('normalized_sha256'))
    admitted = all((request_ok, found_ok, pointer_ok, metadata_ok, origin_ok,
                    edition_ok, binding_ok, body_ok))
    return {'status': 'identity_consistent' if admitted else 'hold',
            'identity_admitted': admitted, 'semantic_support': 'unreviewed',
            'answer_verified': False}


def structured_gate(case: dict, registry: dict) -> dict:
    """Return inspectable per-dimension states and preserve semantic uncertainty."""
    s, f, t = case['selected'], case['fetched'], case['target']
    ref = registry.get(f"{t['document']}:{t['paragraph']}:{t['edition']}:{t['language']}")
    states = {}
    def record(name: str, passed: bool | None) -> None:
        states[name] = 'unknown' if passed is None else ('match' if passed else 'mismatch')
    record('request_binding', None if f.get('requested_id') is None else f['requested_id'] == s.get('id'))
    record('fetch_available', f.get('found') is True)
    record('response_binding', None if not f.get('found') else f.get('returned_id') == s.get('id'))
    a, b = pointer(s.get('url')), pointer(f.get('url'))
    expected = (t['document'], t['paragraph'])
    record('search_document_and_paragraph', None if a is None else a == expected)
    record('fetch_document_and_paragraph', None if b is None else b == expected)
    record('metadata_document', None if f.get('document') is None else f['document'] == t['document'])
    n = paragraph(f.get('ref'))
    record('metadata_paragraph', None if n is None else n == t['paragraph'])
    record('original_locator_receipt', None if ref is None else ref.get('locator_observed') is True)
    record('edition', None if f.get('edition') is None else f['edition'] == t['edition'])
    record('language', None if f.get('language') is None else f['language'] == t['language'])
    related = [x for x in case['search_results'] if x.get('id') == s.get('id')]
    bindings = {pointer(x.get('url')) for x in related}
    record('identifier_uniqueness', None if not related else bindings == {expected})
    body = f.get('body')
    record('payload_correspondence', None if (not isinstance(body, str) or not body.strip() or ref is None)
           else digest(body) == ref.get('normalized_sha256'))
    admitted = all(x == 'match' for x in states.values())
    return {'status': 'identity_consistent' if admitted else 'hold',
            'identity_admitted': admitted, 'states': states,
            'semantic_support': 'unreviewed', 'answer_verified': False}
