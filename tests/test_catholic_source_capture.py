"""Local publication integrity checks, not independent research validation."""
import copy
import hashlib
import json
import runpy
import unittest
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'catholic-ai-pilot'
E=ROOT/'_evidence'
API=runpy.run_path(str(ROOT/'_tools/capture_checks.py'))
class ReadingChecks(unittest.TestCase):
    def setUp(self):
        self.capture=json.loads((E/'runs/SV-20261106-001/capture.json').read_text())
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
        self.assertEqual(hashlib.sha256((E/'sources/normative-crosswalk.json').read_bytes()).hexdigest(),'d9d76d58dc0186e1a5956b66028992845ef5f1b273d3ca1eccdb4f5fa24bf5d0')
    def test_hypotheses_preserved(self):
        current=json.loads((E/'design/study.json').read_text());old=json.loads((E/'design/original-study.json').read_text())
        self.assertEqual(current['hypotheses'],old['hypotheses'])
    def test_source_text_projection(self):
        fetched=self.capture['records'][3]['response']
        self.assertNotIn('text',fetched)
        self.assertLessEqual(len(fetched['text_excerpt'].split()),20)
        self.assertEqual(len(fetched['text_sha256']),64)
if __name__=='__main__':unittest.main(verbosity=2)
