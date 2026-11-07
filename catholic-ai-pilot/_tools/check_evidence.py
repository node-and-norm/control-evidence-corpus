#!/usr/bin/env python3
"""Offline development checks. No network calls and no automatic publication approval.

This intentionally small gate checks record prerequisites, not source truth,
reviewer independence, theological validity, or real-world control effectiveness.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import unittest

ALLOWED_KINDS = {'retrieval_observation', 'normative_mapping', 'empirical_control', 'software_check'}


def assess_claim(claim: dict, evidence: dict, review: dict | None = None) -> list[str]:
    """Return explicit blockers; an empty list still requires human release approval."""
    blockers = []
    if claim.get('kind') not in ALLOWED_KINDS:
        blockers.append('unsupported_claim_kind')
    ids = claim.get('evidence_ids')
    if not isinstance(ids, list) or not ids:
        return blockers + ['no_evidence_links']
    selected = []
    for key in ids:
        if not isinstance(key, str) or key not in evidence:
            blockers.append('unresolved_evidence_reference')
        else:
            selected.append(evidence[key])
    if not isinstance(claim.get('limitations'), list) or not claim['limitations']:
        blockers.append('missing_limitations')
    if claim.get('kind') != 'software_check':
        if any(x.get('origin') in {'synthetic', 'reconstructed_summary'} for x in selected):
            blockers.append('insufficient_evidence_origin')
    if any(x.get('rights_status') != 'cleared' for x in selected):
        blockers.append('rights_review_required')
    if any(x.get('restricted', False) for x in selected):
        blockers.append('restricted_material_publication_blocked')
    if claim.get('kind') == 'normative_mapping':
        if any(x.get('locator_status') != 'verified_original' for x in selected):
            blockers.append('original_locator_verification_required')
        if not review or review.get('kind') != 'qualified_human_normative':
            blockers.append('qualified_normative_review_required')
        elif review.get('status') != 'recorded':
            blockers.append('review_not_recorded')
    if claim.get('kind') == 'empirical_control':
        if not any(x.get('type') in {'operational_record', 'controlled_test'} for x in selected):
            blockers.append('operation_evidence_required')
        if not review or review.get('kind') != 'independent_human_technical':
            blockers.append('independent_human_review_required')
        elif review.get('status') != 'recorded':
            blockers.append('review_not_recorded')
        if not claim.get('conditions'):
            blockers.append('missing_test_or_event_conditions')
    if review and claim.get('unassisted_initial_rating') and review.get('ai_exposure') != 'none':
        blockers.append('unassisted_rating_claim_conflicts_with_exposure')
    if review and claim.get('author_id') and review.get('reviewer_id') == claim['author_id']:
        blockers.append('self_review_is_not_independent')
    if claim.get('outcome_state') in {'unknown', 'not_reported', 'not_observable', 'conflicting'} and claim.get('conclusion') in {'control_absent', 'control_effective'}:
        blockers.append('uncertainty_upgraded_to_categorical_finding')
    if claim.get('raw_failure_count', 0) > 0 and not claim.get('failure_record_ids'):
        blockers.append('failure_records_missing')
    if claim.get('numeric_result') is not None and not isinstance(claim.get('denominator'), int):
        blockers.append('denominator_required')
    elif claim.get('numeric_result') is not None and claim.get('denominator', 0) <= 0:
        blockers.append('invalid_denominator')
    return sorted(set(blockers))


def verify_hashes(root: Path, manifest: dict) -> list[str]:
    """Verify only explicitly listed local files, with traversal protection."""
    errors = []
    resolved_root = root.resolve()
    for row in manifest.get('files', []):
        path = (resolved_root / row['path']).resolve()
        if not path.is_relative_to(resolved_root):
            errors.append('unsafe_path:' + row['path'])
        elif not path.is_file():
            errors.append('missing:' + row['path'])
        elif hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
            errors.append('changed:' + row['path'])
    return errors


class BoundaryTests(unittest.TestCase):
    """Invented software fixtures only; never use these as human-reviewed data."""
    def setUp(self):
        self.e = {'E1': {'origin': 'captured_record', 'type': 'controlled_test', 'rights_status': 'cleared', 'restricted': False, 'locator_status': 'verified_original'}}
        self.c = {'kind': 'empirical_control', 'evidence_ids': ['E1'], 'limitations': ['Fixture only.'], 'conditions': 'Invented bounded test', 'author_id': 'FIXTURE-A', 'outcome_state': 'yes', 'conclusion': 'bounded_observation'}
        self.r = {'kind': 'independent_human_technical', 'status': 'recorded', 'reviewer_id': 'FIXTURE-B', 'ai_exposure': 'none'}
    def test_complete_record_passes_prerequisites_only(self):
        self.assertEqual(assess_claim(self.c,self.e,self.r), [])
    def test_missing_evidence(self):
        self.c['evidence_ids'] = []
        self.assertIn('no_evidence_links',assess_claim(self.c,self.e,self.r))
    def test_dangling_link(self):
        self.c['evidence_ids'] = ['MISSING']
        self.assertIn('unresolved_evidence_reference',assess_claim(self.c,self.e,self.r))
    def test_missing_limitations(self):
        self.c['limitations'] = []
        self.assertIn('missing_limitations',assess_claim(self.c,self.e,self.r))
    def test_synthetic_is_not_empirical(self):
        self.e['E1']['origin'] = 'synthetic'
        self.assertIn('insufficient_evidence_origin',assess_claim(self.c,self.e,self.r))
    def test_summary_is_not_raw_capture(self):
        self.e['E1']['origin'] = 'reconstructed_summary'
        self.assertIn('insufficient_evidence_origin',assess_claim(self.c,self.e,self.r))
    def test_policy_is_not_operating_evidence(self):
        self.e['E1']['type'] = 'policy'
        self.assertIn('operation_evidence_required',assess_claim(self.c,self.e,self.r))
    def test_model_is_not_human_reviewer(self):
        self.r['kind'] = 'model_judge'
        self.assertIn('independent_human_review_required',assess_claim(self.c,self.e,self.r))
    def test_unknown_is_not_absence(self):
        self.c.update(outcome_state='not_reported',conclusion='control_absent')
        self.assertIn('uncertainty_upgraded_to_categorical_finding',assess_claim(self.c,self.e,self.r))
    def test_no_automatic_normative_approval(self):
        self.c['kind'] = 'normative_mapping'
        self.assertIn('qualified_normative_review_required',assess_claim(self.c,self.e,self.r))
    def test_wrong_locator(self):
        self.c['kind'] = 'normative_mapping';self.e['E1']['locator_status'] = 'mismatch'
        self.assertIn('original_locator_verification_required',assess_claim(self.c,self.e,self.r))
    def test_rights_pending(self):
        self.e['E1']['rights_status'] = 'unknown'
        self.assertIn('rights_review_required',assess_claim(self.c,self.e,self.r))
    def test_private_evidence_not_public(self):
        self.e['E1']['restricted'] = True
        self.assertIn('restricted_material_publication_blocked',assess_claim(self.c,self.e,self.r))
    def test_reviewer_exposure(self):
        self.c['unassisted_initial_rating'] = True;self.r['ai_exposure'] = 'prior_suggestion'
        self.assertIn('unassisted_rating_claim_conflicts_with_exposure',assess_claim(self.c,self.e,self.r))
    def test_self_review(self):
        self.r['reviewer_id'] = 'FIXTURE-A'
        self.assertIn('self_review_is_not_independent',assess_claim(self.c,self.e,self.r))
    def test_missing_denominator(self):
        self.c['numeric_result'] = 0.5
        self.assertIn('denominator_required',assess_claim(self.c,self.e,self.r))
    def test_failed_attempts_preserved(self):
        self.c['raw_failure_count'] = 1
        self.assertIn('failure_records_missing',assess_claim(self.c,self.e,self.r))


def run_checks() -> dict:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BoundaryTests)
    result = unittest.TestResult()
    suite.run(result)
    return {'kind': 'software_maintenance_check', 'synthetic_fixtures': True,
            'tests_run': result.testsRun, 'failures': len(result.failures),
            'errors': len(result.errors), 'success': result.wasSuccessful(),
            'checks': [str(x) for x,_ in result.failures + result.errors],
            'scientific_validity_established': False,
            'limit': 'Contract prerequisites only. No source truth, reviewer independence, doctrinal judgment, or safeguard effectiveness certified.'}


if __name__ == '__main__':
    report = run_checks()
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['success'] else 1)
