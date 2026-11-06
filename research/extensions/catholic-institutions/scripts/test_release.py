"""Local publication integrity checks, not independent research validation."""
import copy
import hashlib
import json
import runpy
import unittest
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
API=runpy.run_path(str(ROOT/'scripts/build_release.py'))
class ReadingChecks(unittest.TestCase):
    def setUp(self):
        self.capture=json.loads((ROOT/'runs/SV-20261106-001/capture.json').read_text())
    def test_recorded_pair_outcomes(self):
        self.assertEqual([x['outcome'] for x in API['derive'](self.capture)],['fetch_not_found','locator_mismatch'])
    def test_plan_hash_rejects_change(self):
        self.capture['plan']['max_calls']=5
        with self.assertRaises(ValueError):API['derive'](self.capture)
    def test_unreturned_identifier_rejected(self):
        self.capture['records'][1]['request']['id']='not-returned'
        with self.assertRaises(ValueError):API['derive'](self.capture)
    def test_local_capture_chronology(self):
        plan=datetime.fromisoformat(self.capture['plan']['plan_recorded_at'])
        self.assertTrue(all(datetime.fromisoformat(x['recorded_at'])>plan for x in self.capture['records']))
    def test_normative_bytes_preserved(self):
        self.assertEqual((ROOT/'data/normative-crosswalk.json').read_bytes(),(ROOT/'archive/v0.2/data/normative-crosswalk.json').read_bytes())
    def test_hypotheses_preserved(self):
        current=json.loads((ROOT/'study.json').read_text());old=json.loads((ROOT/'archive/v0.2/study.json').read_text())
        self.assertEqual(current['hypotheses'],old['hypotheses'])
    def test_five_reading_files(self):
        names=['NodeNorm_Study_v0_4_0.pdf','NodeNorm_Study_v0_4_0.html','NodeNorm_Notebook_v0_4_0.ipynb','NodeNorm_Protocol_v0_3_0.html','NodeNorm_Protocol_v0_3_0.md']
        for name in names:self.assertGreater((ROOT/'reading'/name).stat().st_size,200)
    def test_source_text_projection(self):
        fetched=self.capture['records'][3]['response']
        self.assertNotIn('text',fetched)
        self.assertLessEqual(len(fetched['text_excerpt'].split()),20)
        self.assertEqual(len(fetched['text_sha256']),64)
    def test_main_readme_unchanged(self):
        path=ROOT.parents[2]/'README.md'
        if not path.exists():self.skipTest('Full checkout unavailable in local attachment workspace; CI must run this check.')
        data=path.read_bytes();actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        self.assertEqual(actual,json.loads((ROOT/'release.json').read_text())['root_readme_blob_sha1'])
if __name__=='__main__':unittest.main(verbosity=2)
