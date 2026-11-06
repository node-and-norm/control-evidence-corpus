"""Offline replay conformance, not independent scientific validation."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'research/extensions/catholic-institutions/scenario-batches/CB-001/CIR-001'

class CatholicCitationGateReplay(unittest.TestCase):
    def test_frozen_inputs_and_retained_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'replay'
            result = subprocess.run([sys.executable, str(RUN/'reproduce.py'), '--output', str(out)],
                                    check=True, capture_output=True, text=True, timeout=45)
            receipt = json.loads((out/'replay-receipt.json').read_text())
            self.assertTrue(receipt['original_outputs_match'])
            self.assertEqual(receipt['outputs'], 72)
            self.assertEqual(receipt['new_live_observations'], 0)
            self.assertFalse(receipt['independent_validation'])
            rows = json.loads((out/'raw-results.replay.json').read_text())
            for name in ['simple_checklist', 'structured_gate']:
                arm = [x['output'] for x in rows if x['procedure']==name]
                self.assertEqual(sum(x['identity_admitted'] for x in arm), 8)
                self.assertTrue(all(x['semantic_support']=='unreviewed' and not x['answer_verified'] for x in arm))

if __name__ == '__main__':
    unittest.main()
