"""The source-review AI contribution must remain disclosed with pending human approval."""
from pathlib import Path
import json, unittest
R=Path(__file__).resolve().parents[1]/'catholic-ai-pilot'
class SourceReviewAIUse(unittest.TestCase):
 def test_disclosure_and_review_limits(self):
  d=json.loads((R/'_evidence/disclosure/source-review-round1.json').read_text())
  self.assertEqual(d['new_magisterium_chat_calls'],0)
  self.assertEqual(d['related_source_run'],'PARISH-QA-001-R1')
  self.assertFalse(d['independent_validation'])
  self.assertFalse(d['user_authorization_converted_to_reviewer_approval'])
  self.assertEqual(d['human_review_attestations'],[])
  self.assertEqual(d['qualified_canon_law_review'],'pending')
  self.assertIsNone(d['exact_model_snapshot'])
if __name__=='__main__':unittest.main()
