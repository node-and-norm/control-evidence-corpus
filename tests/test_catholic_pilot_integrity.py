"""Maintenance guards, not independent scientific or theological validation."""
from pathlib import Path
import copy,hashlib,json,runpy,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'catholic-ai-pilot'
API=runpy.run_path(str(ROOT/'scripts/check_catholic_pilot.py'))
class CatholicConsolidationTests(unittest.TestCase):
 def test_complete_checkout_contract(self):
  r=API['check']();self.assertEqual(r['notebooks'],16);self.assertEqual(r['original_master_cells_preserved'],40)
  self.assertEqual(r['exact_service_responses'],6);self.assertFalse(r['independent_research_validation'])
 def test_no_duplicate_reader_archive(self):
  self.assertFalse((ROOT/'research/extensions/catholic-institutions').exists())
  self.assertFalse(any(p.suffix in {'.md','.html','.pdf'} for p in B.rglob('*') if p.is_file()))
 def test_source_hash_mutation_is_detectable(self):
  row=json.loads((B/'_provenance/consolidation.json').read_text())['retained_evidence'][0]
  content=(ROOT/row['path']).read_bytes()
  self.assertEqual(hashlib.sha256(content).hexdigest(),row['sha256'])
  self.assertNotEqual(hashlib.sha256(content+b' ').hexdigest(),row['sha256'])
 def test_disclosure_stays_unattested(self):
  r=json.loads((B/'_evidence/disclosure/record.json').read_text())
  for k in ['specific_personal_review_attestations','independent_review_attestations','qualified_theological_review_attestations']:
   self.assertEqual(r['human_review'][k],[])
 def test_full_notebook_is_upfront(self):
  n=json.loads((ROOT/'CATHOLIC_PILOT.ipynb').read_text())
  self.assertEqual(len(n['cells']),42)
  self.assertIn('complete study',''.join(n['cells'][0]['source']).lower())
  self.assertEqual(sum(c['cell_type']=='code' for c in n['cells']),10)
 def test_workflow_and_milestones_visible(self):
  n=json.loads((B/'01_Study_and_Roadmap.ipynb').read_text())
  s='\n'.join(''.join(c['source']) for c in n['cells'])
  for x in ['Discover','Screen','Review','Reconstruct','Evaluate','Report','seven-stage milestone plan']:
   self.assertIn(x,s)
 def test_pending_review_preserved(self):
  r=json.loads((B/'_evidence/scenarios/CB-001/obligations/mappings.json').read_text())
  for m in r['mappings']:
   self.assertEqual(m['assessment']['canonical_applicability'],'pending_qualified_review')
   self.assertEqual(m['assessment']['compliance_conclusion'],'not_assessed')
 def test_replay_inputs_match_original_plan(self):
  r=B/'_evidence/scenarios/CB-001/CIR-001'
  p=json.loads((r/'plan.json').read_text())
  self.assertEqual(hashlib.sha256((r/'engine.py').read_bytes()).hexdigest(),p['input_sha256']['engine.py'])
 def test_book_only_references_notebook_chapters(self):
  toc=json.loads((B/'myst.yml').read_text())['project']['toc']
  self.assertEqual(len(toc),15)
  for row in toc:self.assertTrue((B/row['file']).exists());self.assertTrue(row['file'].endswith('.ipynb'))
 def test_retired_versions_have_a_history_pointer(self):
  r=json.loads((B/'_provenance/consolidation.json').read_text())
  self.assertFalse(r['history_rewritten']);self.assertTrue(r['retired_files'])
  self.assertTrue(all(x['preserved_at_commit']==r['baseline_commit'] for x in r['retired_files']))
BoundaryTests=runpy.run_path(str(B/'_tools/check_evidence.py'))['BoundaryTests']
if __name__=='__main__':unittest.main()
