"""Archived-reader byte and status checks; no model calls or truth judgments."""
from pathlib import Path
import hashlib
import json
import unittest

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / 'research/extensions/catholic-institutions'

class CatholicReaderArchiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads((ROOT/'reading/ARTIFACT_INDEX.json').read_text())

    def test_three_editions_and_latest_pointer(self):
        self.assertEqual(set(self.index['editions']), {'0.4.2-draft','0.4.3-draft','0.4.4-draft'})
        self.assertEqual(self.index['latest_draft'], '0.4.4-draft')
        self.assertEqual(self.index['published_release_preserved'], 'catholic-pilot-v0.4.1-dev')

    def test_all_fifteen_files_match_manifest(self):
        count = 0
        for edition in self.index['editions'].values():
            self.assertEqual(len(edition['files']), 4)
            for record in edition['files'] + [edition['pdf']]:
                path = (ROOT/record['path']).resolve()
                self.assertTrue(path.is_relative_to(ROOT.resolve()))
                data = path.read_bytes()
                self.assertEqual(len(data), record['bytes'])
                self.assertEqual(hashlib.sha256(data).hexdigest(), record['sha256'])
                count += 1
        self.assertEqual(count, 15)

    def test_notebooks_retain_executed_outputs_without_error_records(self):
        for version, expected_cells in [('0.4.2',7),('0.4.3',9),('0.4.4',10)]:
            name = 'NodeNorm_Notebook_v'+version.replace('.','_')+'.ipynb'
            nb = json.loads((ROOT/'reading/editions'/(version+'-draft')/name).read_text())
            cells = [c for c in nb['cells'] if c['cell_type']=='code']
            self.assertEqual(nb['nbformat'],4)
            self.assertEqual(len(cells),expected_cells)
            self.assertTrue(all(isinstance(c.get('execution_count'),int) for c in cells))
            self.assertFalse(any(o.get('output_type')=='error' for c in cells for o in c.get('outputs',[])))

    def test_pdf_origin_is_not_mislabelled(self):
        for edition in self.index['editions'].values():
            pdf = edition['pdf']
            self.assertEqual(pdf['origin'],'repository_render_from_archived_html')
            self.assertIs(pdf['original_attachment_pdf_byte_identity_claimed'],False)
            self.assertTrue((ROOT/pdf['path']).read_bytes().startswith(b'%PDF-'))
            html = next(x for x in edition['files'] if '/NodeNorm_Study_' in x['path'])
            self.assertEqual(pdf['source_html_sha256'],html['sha256'])

    def test_replay_is_not_new_research_or_independent_review(self):
        self.assertFalse(self.index['new_research_results'])
        self.assertEqual(self.index['qualified_review'],'pending')
        for edition in self.index['editions'].values():
            replay = edition['replay_check']
            self.assertTrue(replay['offline_replay_completed'])
            self.assertTrue(replay['archive_unchanged'])
            self.assertEqual(replay['new_model_or_service_calls'],0)
            self.assertFalse(replay['independent_validation'])

    def test_root_readme_remains_protected(self):
        data = (REPO/'README.md').read_bytes()
        import runpy
        data = runpy.run_path(str(REPO/'scripts/build_catholic_notebook_book.py'))['strip_navigation'](data)
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        self.assertEqual(blob,'27ce767242321634d9048eea87ffa31697e3877c')

if __name__ == '__main__':
    unittest.main()
