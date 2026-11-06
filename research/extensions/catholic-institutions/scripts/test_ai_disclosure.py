"""Disclosure integrity checks. Invented mutations, no scientific validation."""
import copy
import json
from pathlib import Path
import runpy
import unittest
ROOT=Path(__file__).resolve().parent.parent
API=runpy.run_path(str(ROOT/'scripts/apply_ai_disclosure.py'))
class DisclosureChecks(unittest.TestCase):
    def setUp(self):
        self.r=json.loads((ROOT/'disclosure/record.json').read_text())
    def test_current_record_consistent(self):
        self.assertEqual(API['validate_record'](self.r),[])
    def test_no_inferred_model(self):
        self.r['tools'][0]['unknown_reason']=''
        self.assertIn('unknown_model_without_reason',API['validate_record'](self.r))
    def test_no_ai_authorship(self):
        self.r['publication']['ai_authors']=['AI']
        self.assertIn('ai_cannot_be_author',API['validate_record'](self.r))
    def test_no_blanket_approval(self):
        self.r['human_review']['authorization_is_source_verification']=True
        self.assertIn('authorization_overclaim',API['validate_record'](self.r))
    def test_no_venue_no_compliance(self):
        self.r['publication']['venue_compliance']='compliant'
        self.assertIn('venue_compliance_without_venue',API['validate_record'](self.r))
    def test_contribution_needs_scope(self):
        self.r['contributions'][0]['artifact_scope']=[]
        self.assertIn('contribution_without_scope_or_basis',API['validate_record'](self.r))
    def test_tool_reference(self):
        self.r['contributions'][0]['tools']=['UNKNOWN']
        self.assertIn('unknown_tool_reference',API['validate_record'](self.r))
    def test_review_status(self):
        self.r['contributions'][0]['human_review_status']=''
        self.assertIn('review_status_missing',API['validate_record'](self.r))
    def test_fake_attestation(self):
        self.r['human_review']['independent_review_attestations']=[{'reviewer':'Example'}]
        self.assertIn('incomplete_human_attestation',API['validate_record'](self.r))
    def test_no_historical_prompt_invention(self):
        self.r['retention']['historical_prompt_reconstruction_permitted']=True
        self.assertIn('unsafe_retention_claim:historical_prompt_reconstruction_permitted',API['validate_record'](self.r))
    def test_no_public_secrets(self):
        self.r['retention']['public_secrets_permitted']=True
        self.assertIn('unsafe_retention_claim:public_secrets_permitted',API['validate_record'](self.r))
    def test_history_separate(self):
        history=json.loads((ROOT/'disclosure/historical-guidance-2026-10-27.json').read_text())
        checks=json.loads((ROOT/'disclosure/policy-checks.json').read_text())
        self.assertEqual([r['rule_id'] for r in history['rows']],['DR-002','DR-003','DR-004','DR-005','DR-011'])
        self.assertTrue(all(r['checked_utc']=='2026-10-27' for r in history['rows']))
        self.assertEqual(checks['checked_utc_date'],'2026-11-06')
    def test_idempotent_html(self):
        p=json.loads((ROOT/'disclosure/policy-checks.json').read_text())
        text=API['markdown'](self.r,p)
        base='<html><head><style>body{color:black}</style></head><body><main><h1>Study</h1></main></body></html>'
        once=API['patch_html'](base,self.r,p,text)
        self.assertEqual(once,API['patch_html'](once,self.r,p,text))
    def test_actual_record_has_no_human_attestations(self):
        for k in ['specific_personal_review_attestations','independent_review_attestations','qualified_theological_review_attestations']:
            self.assertEqual(self.r['human_review'][k],[])
    def test_deterministic_statement(self):
        p=json.loads((ROOT/'disclosure/policy-checks.json').read_text())
        self.assertEqual(API['markdown'](self.r,p),API['markdown'](copy.deepcopy(self.r),copy.deepcopy(p)))
if __name__=='__main__':unittest.main(verbosity=2)
