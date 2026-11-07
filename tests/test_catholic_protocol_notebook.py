"""Presentation fidelity checks, not scientific or theological validation."""
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parents[1]
API = runpy.run_path(str(ROOT / 'research/extensions/catholic-institutions/scripts/build_protocol_notebook.py'))


class ProtocolNotebookTests(unittest.TestCase):
    def setUp(self):
        self.raw = API['SOURCE'].read_bytes()
        self.nb = API['generate'](self.raw)

    def test_complete_source_roundtrip(self):
        self.assertEqual(API['reassemble'](self.nb), self.raw)

    def test_changed_source_is_rejected(self):
        with self.assertRaises(ValueError):
            API['generate'](self.raw + b'\n')

    def test_narrative_cells_have_no_executed_results(self):
        self.assertTrue(all(c['cell_type'] == 'markdown' for c in self.nb['cells']))
        self.assertTrue(all('outputs' not in c and 'execution_count' not in c for c in self.nb['cells']))

    def test_cell_identifiers_are_unique(self):
        ids = [c['id'] for c in self.nb['cells']]
        self.assertEqual(len(ids), len(set(ids)))

    def test_generation_is_deterministic(self):
        self.assertEqual(API['serialize'](self.nb), API['serialize'](API['generate'](self.raw)))

    def test_core_protocol_and_review_boundary_preserved(self):
        m = self.nb['metadata']['node_norm']
        self.assertEqual(m['core_protocol'], '0.3.0; unfrozen')
        self.assertEqual(m['qualified_review'], 'pending')
        self.assertFalse(m['new_research_results'])

    def test_source_offsets_and_hashes(self):
        position = 0
        for cell in self.nb['cells']:
            m = cell['metadata']['node_norm']
            if m['role'] != 'archived_source':
                continue
            text = ''.join(cell['source'])
            self.assertEqual(m['character_start'], position)
            self.assertEqual(m['source_chunk_sha256'], API['sha'](text.encode()))
            position += len(text)
        self.assertEqual(position, len(self.raw.decode('utf-8')))

    def test_generated_copy_when_present(self):
        if not API['OUTPUT'].is_file():
            self.skipTest('Reader generation has not committed its copy yet.')
        API['build'](check=True)


if __name__ == '__main__':
    unittest.main()
