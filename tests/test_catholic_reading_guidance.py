"""Presentation/instruction checks; no new study or provider requests."""
from pathlib import Path
import ast
import contextlib
import io
import json
import re
import socket
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'catholic-ai-pilot'


def cell_text(cell):
    return ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']


class CatholicReadingGuidance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guide = json.loads((BOOK / '09_Reproduce_and_Inspect.ipynb').read_text(encoding='utf-8'))
        cls.root = json.loads((ROOT / 'CATHOLIC_PILOT.ipynb').read_text(encoding='utf-8'))
        cls.text = '\n\n'.join(cell_text(c) for c in cls.guide['cells'])

    def test_guide_is_nonexecuting_notebook_with_distinct_sections(self):
        self.assertEqual(self.guide['nbformat'], 4)
        self.assertTrue(all(c['cell_type'] == 'markdown' for c in self.guide['cells']))
        self.assertEqual(len({c['id'] for c in self.guide['cells']}), len(self.guide['cells']))
        self.assertIn('No installation or command is required', self.text)
        self.assertIn('not executable Python notebook cells', self.text)
        self.assertFalse(self.guide['metadata']['node_norm']['new_research_results'])

    def test_installation_precedes_checks_and_includes_runtime(self):
        install = "python -m pip install '.[agents]'"
        check = 'python scripts/check_catholic_pilot.py'
        self.assertLess(self.text.index(install), self.text.index(check))
        self.assertEqual(self.text.count('python -m pip install'), 1)
        self.assertIn('Python 3.11', self.text)
        self.assertIn('Git clone with its history', self.text)
        self.assertIn('Package installation can use the internet', self.text)
        self.assertIn('not Python source to paste', self.text)

    def test_shell_blocks_are_balanced_and_script_paths_exist(self):
        for cell in self.guide['cells']:
            text = cell_text(cell)
            self.assertEqual(text.count('```') % 2, 0)
            blocks = re.findall(r'```([^\n]*)\n(.*?)\n```', text, flags=re.S)
            for lang, source in blocks:
                self.assertEqual(lang, 'bash')
                flattened = source.replace('\\\n', ' ')
                for line in flattened.splitlines():
                    self.assertTrue(line.startswith('python '), line)
                    command = line.split()
                    if command[1].endswith('.py'):
                        self.assertTrue((ROOT / command[1]).is_file(), command[1])

    def test_long_source_and_saved_outputs_are_complete(self):
        code = [c for c in self.root['cells'] if c['cell_type'] == 'code']
        self.assertEqual(len(code), 10)
        for c in code:
            ast.parse(cell_text(c))
            self.assertFalse(any(o['output_type'] == 'error' for o in c.get('outputs', [])))
        first = next(c for c in code if c['id'] == '67cc94a3')
        self.assertEqual(max(map(len, cell_text(first).splitlines())), 21177)
        saved = ''.join(''.join(o['text']) if isinstance(o['text'], list) else o['text']
                        for o in first['outputs'] if o['output_type'] == 'stream')
        values = json.loads(saved)
        self.assertEqual((values['cases'], values['reference_entries'], values['unique_reference_urls']), (6, 40, 38))
        self.assertFalse(values['qualified_correctness_established'])
        self.assertFalse(values['compliance_assessed'])
        self.assertEqual(values['network_calls'], 0)
        with patch.object(socket.socket, 'connect', side_effect=AssertionError('network denied')):
            with patch('socket.create_connection', side_effect=AssertionError('network denied')):
                with contextlib.redirect_stdout(io.StringIO()) as captured:
                    exec(compile(cell_text(first), 'first_preserved_integrity_cell.py', 'exec'), {})
        self.assertEqual(captured.getvalue(), saved)


if __name__ == '__main__':
    unittest.main()
