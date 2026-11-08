"""Bounded prior-work review and unfrozen study proposal checks; no scientific validation."""
from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1];BOOK=ROOT/'catholic-ai-pilot'
class CatholicPriorWorkScreen(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.reg=json.loads((BOOK/'_evidence/reviews/prior-work-and-next-test-20261108.json').read_text())
  cls.dis=json.loads((BOOK/'_evidence/disclosure/prior-work-20261108.json').read_text())
  cls.nb=json.loads((BOOK/'15_Prior_Work_and_Next_Evaluation.ipynb').read_text())
 def test_works_sources_and_distinct_doi(self):
  p=self.reg['papers']
  self.assertEqual(len(p),7)
  self.assertEqual(len({x['key'] for x in p}),7)
  self.assertEqual(len({x['doi'] for x in p}),7)
  self.assertTrue(all(x['url'].startswith('https://') and x['reviewed'] for x in p))
  txt='\n'.join(''.join(c['source']) if isinstance(c['source'],list) else c['source'] for c in self.nb['cells'])
  self.assertTrue(all(x['url'] in txt for x in p))
 def test_design_unfrozen_and_independent_review_pending(self):
  d=self.reg['planned_study']
  self.assertEqual(d['status'],'proposal_only_unfrozen')
  self.assertTrue(d['no_case_generation_or_execution'])
  self.assertTrue(d['must_freeze_before_run'])
  self.assertTrue(d['falsification_conditions'])
  self.assertIn('checklist',d['baseline'].lower())
  self.assertEqual(self.dis['new_magisterium_calls'],0)
  self.assertEqual(self.dis['new_model_evaluation_calls'],0)
  self.assertEqual(self.dis['independent_expert_attestations'],[])
  self.assertFalse(self.dis['independent_novelty_verification'])
 def test_notebook_study_scope(self):
  self.assertEqual(self.nb['nbformat'],4)
  self.assertTrue(all(c['cell_type']=='markdown' for c in self.nb['cells']))
  self.assertEqual(len({c['id'] for c in self.nb['cells']}),len(self.nb['cells']))
  self.assertEqual(self.nb['metadata']['node_norm']['new_experiments'],0)
  self.assertEqual(self.nb['metadata']['node_norm']['qualified_review'],'pending')
 def test_cir_result_disclosure(self):
  p=self.reg['prior_internal_result']
  self.assertEqual(p['case_count'],24)
  self.assertEqual(p['valid_identity_retained_both'],8)
  self.assertEqual(p['non_admissible_held_both'],16)
  self.assertEqual(p['meaning_review'],'unreviewed')
if __name__=='__main__':unittest.main()
