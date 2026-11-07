"""Notebook book custody checks. Standard library only; no research calls."""
from pathlib import Path
import collections
import hashlib
import json
import re
import runpy
import unittest

ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'catholic-ai-pilot'

def read_nb(path):return json.loads(path.read_text())
def text(cell):return ''.join(cell.get('source',[])) if isinstance(cell.get('source'),list) else cell.get('source','')

class CatholicNotebookBookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=BOOK/'_provenance/book-manifest.json'
        if not path.exists():raise unittest.SkipTest('Notebook build has not yet committed its output; the book workflow is the required build gate.')
        cls.manifest=json.loads(path.read_text())
        cls.pages=[ROOT/'CATHOLIC_PILOT.ipynb']+[ROOT/x['path'] for x in cls.manifest['chapters']]

    def test_front_door_and_twelve_chapters(self):
        self.assertEqual(len(self.manifest['chapters']),12)
        for path in self.pages:
            self.assertTrue(path.is_file())
            self.assertEqual(read_nb(path)['nbformat'],4)
        self.assertIn('CATHOLIC_PILOT.ipynb',(ROOT/'README.md').read_text())

    def test_no_standalone_markdown_or_html_reader_pages(self):
        self.assertFalse(list(BOOK.rglob('*.md')))
        self.assertFalse(list(BOOK.rglob('*.html')))
        self.assertFalse(list(BOOK.rglob('*.pdf')))

    def test_all_imported_source_text_preserved(self):
        chunks=collections.defaultdict(list)
        for path in self.pages[1:]:
            for c in read_nb(path)['cells']:
                m=c.get('metadata',{}).get('node_norm',{})
                if m.get('kind')=='source_text':chunks[m['source_path']].append((m['section'],m['original_text']))
        expected={x['source']:x for x in self.manifest['source_documents']}
        self.assertEqual(set(chunks),set(expected))
        self.assertGreaterEqual(len(chunks),25)
        for path, parts in chunks.items():
            raw=''.join(s for _,s in sorted(parts)).encode()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),expected[path]['sha256'])

    def test_local_navigation_resolves_to_notebooks_or_assets(self):
        for path in self.pages:
            for cell in read_nb(path)['cells']:
                if cell['cell_type']!='markdown':continue
                for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text(cell)):
                    if '://' in link or link.startswith(('#','mailto:','attachment:')):continue
                    name=link.split('#')[0].split('?')[0]
                    if not name:continue
                    target=(path.parent/name).resolve()
                    self.assertTrue(target.is_relative_to(ROOT))
                    self.assertTrue(target.exists(),link)
                    self.assertNotIn(target.suffix,{'.md','.html','.pdf'})

    def test_complete_external_answers_visible(self):
        original=json.loads((ROOT/'research/extensions/catholic-institutions/scenario-batches/CB-001/PARISH-QA-001-R1/evidence.json').read_text())
        visible='\n'.join(text(c) for c in read_nb(BOOK/'05_Live_Parish_Responses.ipynb')['cells'] if c['cell_type']=='markdown')
        self.assertEqual(len(original['records']),6)
        for row in original['records']:
            self.assertIn(row['prompt'],visible)
            self.assertIn(row['response']['answer'],visible)

    def test_stored_code_checks_have_outputs_without_errors(self):
        code=[c for p in self.pages for c in read_nb(p)['cells'] if c['cell_type']=='code']
        self.assertEqual(len(code),3)
        for c in code:
            self.assertIsInstance(c['execution_count'],int)
            self.assertTrue(c['outputs'])
            self.assertFalse(any(x['output_type']=='error' for x in c['outputs']))

    def test_root_readme_only_has_exact_authorized_navigation(self):
        b=runpy.run_path(str(ROOT/'scripts/build_catholic_notebook_book.py'))
        current=(ROOT/'README.md').read_bytes()
        self.assertEqual(current.count(b['NAV'].encode()),1)
        original=b['strip_navigation'](current)
        blob=hashlib.sha1(b'blob '+str(len(original)).encode()+b'\0'+original).hexdigest()
        self.assertEqual(blob,'27ce767242321634d9048eea87ffa31697e3877c')

    def test_book_configuration_only_uses_notebooks(self):
        toc=json.loads((BOOK/'myst.yml').read_text())['project']['toc']
        self.assertEqual(len(toc),12)
        for row in toc:self.assertTrue(row['file'].endswith('.ipynb'))

    def test_presentation_not_scientific_release(self):
        self.assertFalse(self.manifest['new_research_results'])
        self.assertEqual(self.manifest['qualified_review'],'pending')
        self.assertEqual(self.manifest['source_mode'],'git_commit')
        self.assertEqual(self.manifest['protocol'],'0.3.0; unfrozen')
        self.assertEqual(self.manifest['new_standalone_markdown_or_html_readers'],0)

if __name__=='__main__':unittest.main()
