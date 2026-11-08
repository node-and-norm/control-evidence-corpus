"""Prospective human review instrument and AI-assisted source-audit custody tests."""
from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]; B=ROOT/'catholic-ai-pilot'
class SourceReviewRoundOne(unittest.TestCase):
 def test_six_cases_nineteen_unique_provisional_claims(self):
  j=json.loads((B/'_evidence/reviews/PARISH-QA-001-R1/claim-review-round1.json').read_text())
  o=json.loads((B/'_evidence/scenarios/CB-001/PARISH-QA-001-R1/evidence.json').read_text())
  cases={x['case_id'] for x in o['records']}; self.assertEqual(len(cases),6)
  self.assertEqual(len(j['claims']),19); self.assertEqual({x['case_id'] for x in j['claims']},cases)
  self.assertEqual(len({x['claim_id'] for x in j['claims']}),19)
  ids={x['id'] for x in j['sources']}
  self.assertTrue(all(set(x['source_ids'])<=ids for x in j['claims']))
 def test_review_not_approved_or_independent(self):
  j=json.loads((B/'_evidence/reviews/PARISH-QA-001-R1/claim-review-round1.json').read_text())
  self.assertTrue(all(x['independent_human_review']=='pending' and x['ecclesial_authority_approval']=='not_sought' for x in j['claims']))
  self.assertEqual(j['next_experiment_design']['status'],'design_candidate_unfrozen')
  self.assertIn('after observing',j['design'])
 def test_secondary_source_distinction(self):
  j=json.loads((B/'_evidence/reviews/PARISH-QA-001-R1/claim-review-round1.json').read_text())
  for x in j['sources']:
   if x['source_kind']=='secondary_locator':self.assertTrue(x['verified_for_this_packet'].startswith('secondary_locator_only'))
 def test_reviewer_packet_contains_unrated_originals(self):
  o=json.loads((B/'_evidence/scenarios/CB-001/PARISH-QA-001-R1/evidence.json').read_text())
  n=json.loads((B/'13_Reviewer_Starting_Packet.ipynb').read_text())
  t='\n'.join(''.join(c['source']) for c in n['cells'])
  for r in o['records']:
   self.assertIn(r['prompt'],t);self.assertIn(r['response']['answer'],t)
  self.assertNotIn('QV-001',t)
  self.assertTrue(all(c['cell_type']=='markdown' for c in n['cells']))
if __name__=='__main__':unittest.main()
