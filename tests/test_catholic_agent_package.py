"""Architecture regression tests; not independent safety or research validation."""
from pathlib import Path
import ast,copy,hashlib,importlib.util,json,os,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
HAS_GRAPH=importlib.util.find_spec('langgraph') is not None
class PackageStaticTests(unittest.TestCase):
 def test_single_trace_implementation(self):
  p=json.loads((ROOT/'specs/agent-team/runtime-layout.json').read_text())
  b=(ROOT/'src/cec_agents/tracing.py').read_bytes()
  self.assertEqual(hashlib.sha256(b).hexdigest(),p['baseline_modules']['catholic-ai-pilot/_tools/prompt_trace.py'])
  shim=(ROOT/'catholic-ai-pilot/_tools/prompt_trace.py').read_text()
  self.assertIn('from cec_agents.tracing import',shim)
  self.assertNotIn('def record_call(',shim)
 def test_no_archived_evidence_changed(self):
  p=json.loads((ROOT/'catholic-ai-pilot/_provenance/runtime-refactor.json').read_text())
  for rel,expected in p['protected_file_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest(),expected,rel)
 def test_no_duplicate_spec_prompts(self):
  for f in (ROOT/'src/cec_agents').rglob('*'):
   if f.is_file():self.assertNotIn(f.suffix,{'.json','.ipynb','.yaml','.yml'})
  spec=json.loads((ROOT/'catholic-ai-pilot/_evidence/agent-team/spec.json').read_text())
  text='\n'.join(p.read_text() for p in (ROOT/'src/cec_agents').glob('*.py'))
  for r in spec['roles']:self.assertNotIn(r['prompt'],text)
 def test_src_install_declared(self):
  import tomllib
  d=tomllib.loads((ROOT/'pyproject.toml').read_text())
  self.assertEqual(d['tool']['setuptools']['packages']['find']['where'],['src'])
  self.assertEqual(d['project']['optional-dependencies']['agents'],['langgraph==1.2.22'])
 def test_existing_notebook_paths_and_outputs(self):
  original=json.loads((ROOT/'catholic-ai-pilot/_provenance/consolidation.json').read_text())
  nb=json.loads((ROOT/'CATHOLIC_PILOT.ipynb').read_text())
  self.assertEqual(len(nb['cells'][2:]),original['root_complete_notebook']['original_cells'])
  n=json.loads((ROOT/'catholic-ai-pilot/17_Agent_Team_and_Assurance.ipynb').read_text())
  self.assertEqual(sum(x['cell_type']=='code' for x in n['cells']),1)
 def test_disclosure_and_approval_boundary(self):
  d=json.loads((ROOT/'catholic-ai-pilot/_provenance/runtime-refactor.json').read_text())
  self.assertFalse(d['issue_41_completed']);self.assertFalse(d['publication_enabled'])
  self.assertEqual(d['ai_use']['human_review_attestations'],[])
  self.assertFalse(d['independent_validation'])

@unittest.skipUnless(HAS_GRAPH,'Graph optional; required in dedicated installed-wheel CI')
class PackageRuntimeTests(unittest.TestCase):
 def test_full_baseline_equivalence(self):
  spec=importlib.util.spec_from_file_location('cec_package_comparison',ROOT/'scripts/check_catholic_agent_package.py')
  mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
  report=mod.compare(baseline_dir=os.environ.get('CEC_BASELINE_DIR'))
  self.assertEqual(report['checks_passed'],12)
  self.assertEqual(report['live_model_calls'],0)
 def test_changed_spec_refused(self):
  from cec_agents.contracts import load_spec
  from cec_agents.capabilities import TeamBlocked
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'spec.json';p.write_text('{}')
   with self.assertRaises(TeamBlocked):load_spec(p,'0'*64)
 def test_core_requires_explicit_inputs(self):
  from cec_agents.workflow import OfflineAgentTeam
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(TypeError):OfflineAgentTeam(Path(d)/'run')
 def test_read_only_lookup_is_detached(self):
  from cec_agents.adapters import LocalPacketAdapter
  from cec_agents.roles import synthetic_packet
  spec=json.loads((ROOT/'catholic-ai-pilot/_evidence/agent-team/spec.json').read_text())
  packet=synthetic_packet();ids={s['id'] for s in packet['sources']}
  a=LocalPacketAdapter(spec,packet,ids);r=a.lookup('SYN-RISK-01');r['text']='mutated'
  self.assertNotEqual(a.lookup('SYN-RISK-01')['text'],'mutated')
if __name__=='__main__':unittest.main()
