"""Offline source-map integrity checks, not legal or scientific validation."""
from pathlib import Path
import json
import unittest
ROOT=Path(__file__).resolve().parent

def load(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

class Integrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=load('sources.json');cls.m=load('mappings.json');cls.p=load('parish-test-plan.json')
    def test_source_ids_unique(self):
        ids=[s['id'] for s in self.s['sources']];self.assertEqual(len(ids),len(set(ids)))
    def test_five_existing_scenarios(self):
        self.assertEqual({x['scenario_id'] for x in self.m['mappings']},{f'CIR-{i:03d}' for i in range(1,6)})
    def test_links_resolve(self):
        ids={x['id'] for x in self.s['sources']}
        for x in self.m['mappings']+self.p['cases']:self.assertTrue(set(x['source_ids'])<=ids)
    def test_canonical_approval_not_inferred(self):
        for x in self.m['mappings']:
            a=x['assessment'];self.assertEqual(a['canonical_applicability'],'pending_qualified_review');self.assertIsNone(a['approval_record']);self.assertIsNone(a['qualified_reviewer']);self.assertFalse(a['ecclesial_endorsement'])
    def test_context_not_invented(self):
        for x in self.m['mappings']:
            a=x['assessment']
            for k in ['institution','diocese','country_or_civil_jurisdiction']:self.assertIsNone(a[k])
            self.assertEqual(a['compliance_conclusion'],'not_assessed')
    def test_three_source_kinds(self):
        self.assertEqual({x['kind'] for x in self.s['sources']},{'canonical_law','amending_legislation','magisterial_teaching'})
    def test_source_hashes_honest(self):
        for x in self.s['sources']:self.assertIsNone(x['source_sha256']);self.assertTrue(x['source_hash_reason'])
    def test_pairs_have_benign_controls(self):
        self.assertEqual(len(self.p['cases']),6)
        for pair in ['privacy','publication','role']:
            c=[x for x in self.p['cases'] if x['pair']==pair];self.assertEqual(len(c),2);self.assertEqual(sum(x['kind']=='benign' for x in c),1)
    def test_no_execution_claim(self):
        self.assertEqual(self.p['run_count'],0);self.assertEqual(self.p['outputs'],[]);self.assertIsNone(self.p['system_under_test'])
        for c in self.p['cases']:self.assertIsNone(c['response'])
    def test_no_semantic_certification(self):
        for c in self.p['cases']:self.assertEqual(c['canonical_judgment'],'pending')
    def test_controls_are_proposals(self):
        self.assertEqual(self.m['controls_are'],'researcher_proposals_not_explicit_software_requirements_in_the_sources')
        for x in self.m['mappings']:self.assertTrue(x['inference_limit'])
    def test_amendment_reference_present(self):
        source=next(x for x in self.s['sources'] if x['id']=='SRC-CQD-2022')
        self.assertIn('15 February 2022',source['source_paraphrase']);self.assertIn('c. 827',source['interpretive_limit'])

if __name__=='__main__':unittest.main(verbosity=2)
