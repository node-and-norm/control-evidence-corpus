"""Check complete notebook import coverage and the visible prose transformation."""
from pathlib import Path
import json
import runpy
import unittest

ROOT=Path(__file__).resolve().parents[1]
EXT=ROOT/'research/extensions/catholic-institutions'
BOOK=ROOT/'catholic-ai-pilot'

def text(cell):
    s=cell.get('source','')
    return ''.join(s) if isinstance(s,list) else s

class VisibleNotebookTextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (BOOK/'_provenance/book-manifest.json').is_file():
            raise unittest.SkipTest('Book generation must precede these checks.')
        cls.manifest=json.loads((BOOK/'_provenance/book-manifest.json').read_text())
        cls.builder=runpy.run_path(str(ROOT/'scripts/build_catholic_notebook_book.py'))

    def test_every_active_source_document_has_a_notebook_destination(self):
        expected={str(p.relative_to(ROOT)) for p in EXT.rglob('*.md')
                  if not str(p.relative_to(EXT)).startswith(('archive/','reading/editions/'))}
        actual={x['source'] for x in self.manifest['source_documents']}
        self.assertEqual(actual,expected)

    def test_visible_prose_matches_original_with_only_declared_link_changes(self):
        prefix='research/extensions/catholic-institutions/'
        mapping={r['source'].removeprefix(prefix):int(r['chapter'][:2])
                 for r in self.manifest['source_documents']}
        mapping.update({'study-report.html':1,'study-guide.ipynb':1,'protocol.html':2})
        checked=0
        for row in self.manifest['chapters']:
            nb=json.loads((ROOT/row['path']).read_text())
            for cell in nb['cells']:
                meta=cell.get('metadata',{}).get('node_norm',{})
                if meta.get('kind')!='source_text':continue
                expected=self.builder['retarget'](meta['original_text'],meta['source_path'].removeprefix(prefix),mapping)
                self.assertEqual(text(cell),expected,meta['source_path'])
                checked+=1
        self.assertGreater(checked,30)

if __name__=='__main__':unittest.main()
