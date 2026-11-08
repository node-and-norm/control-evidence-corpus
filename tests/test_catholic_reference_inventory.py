"""Offline inventory fidelity checks; no Magisterium requests or source-truth judgment."""
from pathlib import Path
from urllib.parse import urlsplit
import hashlib,json,unittest
ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'catholic-ai-pilot'
class ReferenceInventoryChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=(BOOK/'_evidence/scenarios/CB-001/PARISH-QA-001-R1/evidence.json').read_bytes()
  cls.data=json.loads(cls.raw)
  cls.nb=json.loads((BOOK/'14_Reference_Inventory.ipynb').read_text())
  cls.refs=[(r['case_id'],i,x) for r in cls.data['records'] for i,x in enumerate(r['response']['references'],1)]
 def test_source_and_provenance(self):
  p=self.nb['metadata']['node_norm']
  blob=hashlib.sha1(b'blob '+str(len(self.raw)).encode()+b'\0'+self.raw).hexdigest()
  self.assertEqual(p['source_blob_sha1'],blob)
  self.assertEqual(p['source_run'],self.data['run_id'])
  self.assertTrue(p['presentation_only'])
  d=json.loads((BOOK/'_evidence/disclosure/reference-inventory-20261107.json').read_text())
  self.assertEqual(d['new_magisterium_chat_calls'],0)
  self.assertFalse(d['bibliographic_truth_verified'])
  self.assertEqual(d['human_review_attestations'],[])
  self.assertTrue(p['no_new_service_calls'])
 def test_counts(self):
  self.assertEqual(len(self.refs),40)
  self.assertEqual(len({v['source_url'] for _,_,v in self.refs}),38)
  self.assertEqual(len({v['document_title'] for _,_,v in self.refs}),22)
  self.assertEqual(sum(not v.get('document_author','').strip() for _,_,v in self.refs),14)
 def test_original_occurrences_are_in_reader(self):
  body='\n'.join(''.join(c['source']) if isinstance(c['source'],list) else c['source'] for c in self.nb['cells'])
  for case,i,v in self.refs:
   self.assertIn('## '+case,body)
   self.assertIn(v['source_url'],body)
   self.assertIn(v['document_title'].replace('|','\\|'),body)
   self.assertTrue(urlsplit(v['source_url']).scheme=='https')
  self.assertEqual(len({c['id'] for c in self.nb['cells']}),len(self.nb['cells']))
  self.assertTrue(all(c['cell_type']=='markdown' for c in self.nb['cells']))
 def test_no_authoritative_verification_claim(self):
  self.assertEqual(self.nb['metadata']['node_norm']['qualified_reviews'],'pending')
  self.assertEqual(len(self.data['records']),6)
if __name__=='__main__':unittest.main()
