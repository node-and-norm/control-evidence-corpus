"""Application-visible record integrity, not theological validation."""
import copy,json,runpy,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'research/extensions/catholic-institutions/scenario-batches/CB-001'
R=B/'PARISH-QA-001-R1'
class ParishObservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api=runpy.run_path(str(R/'reproduce.py'))
        cls.e=json.loads((R/'evidence.json').read_text())
        cls.d=json.loads((B/'obligations/parish-test-plan.json').read_text())
    def test_six_captured_responses(self):
        x=self.api['check'](self.e,self.d)
        self.assertEqual((x['cases'],x['reference_entries'],x['unique_reference_urls']),(6,40,38))
        self.assertFalse(x['qualified_correctness_established'])
    def test_prompt_mutation_rejected(self):
        x=copy.deepcopy(self.e);x['records'][0]['prompt']='changed'
        with self.assertRaises(AssertionError):self.api['check'](x,self.d)
    def test_invented_review_score_rejected(self):
        x=copy.deepcopy(self.e);x['records'][0]['correctness_score']=1.0
        with self.assertRaises(AssertionError):self.api['check'](x,self.d)
    def test_missing_response_rejected(self):
        x=copy.deepcopy(self.e);x['records'].pop()
        with self.assertRaises(AssertionError):self.api['check'](x,self.d)
if __name__=='__main__':unittest.main()
