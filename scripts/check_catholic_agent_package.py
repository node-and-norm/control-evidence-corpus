#!/usr/bin/env python3
"""Compare installed runtime with a fixed predecessor. No research/network calls.

The baseline is reconstructed temporarily from Git, never archived twice in the
checkout. Normalize only client timestamps, their chain hashes and temp paths.
"""
from __future__ import annotations
import argparse,copy,hashlib,importlib.util,json,os,socket,subprocess,sys,tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
BASE='ab5140f9b80d84380186496c0d89c7f6323de5b6'
SHA=lambda b:hashlib.sha256(b).hexdigest()

def load_module(name,path):
 spec=importlib.util.spec_from_file_location(name,path)
 mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod)
 return mod

def baseline_bytes(path,baseline_dir=None):
 if baseline_dir is not None:return (Path(baseline_dir)/path).read_bytes()
 return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)

def normalized_events(events):
 return [{k:v for k,v in row.items() if k not in {'recorded_at_utc','previous_sha256','event_sha256'}} for row in events]

def normalized_run(report):
 obj=copy.deepcopy(report)
 obj['events']=normalized_events(obj['events'])
 obj['trace_integrity'].pop('run_dir',None);obj['trace_integrity'].pop('last_sha256',None)
 return obj

def compare(*,expect_installed=False,baseline_dir=None):
 import cec_agents
 from cec_agents import tracing
 from cec_agents.workflow import OfflineAgentTeam,run_demo
 from cec_agents.contracts import load_spec
 layout=json.loads((ROOT/'specs/agent-team/runtime-layout.json').read_text())
 specrow=layout['frozen_behavior_spec']
 spec=load_spec(ROOT/specrow['path'],specrow['file_sha256'])
 location=Path(cec_agents.__file__).resolve()
 if expect_installed:
  if location.is_relative_to((ROOT/'src').resolve()) or not location.is_relative_to(Path(sys.prefix).resolve()):
   raise AssertionError('Package was not imported from the installed wheel: '+str(location))
 before={p.relative_to(ROOT).as_posix():SHA(p.read_bytes()) for p in (ROOT/'catholic-ai-pilot').rglob('*') if p.is_file() and p.suffix!='.pyc'}
 checks=[]
 with tempfile.TemporaryDirectory() as td:
  temporary=Path(td);legacyroot=temporary/'legacy'
  for rel,expected in layout['baseline_modules'].items():
   raw=baseline_bytes(rel,baseline_dir)
   if SHA(raw)!=expected:raise AssertionError('Baseline module mismatch: '+rel)
   target=legacyroot/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
  src=legacyroot/specrow['path'];src.parent.mkdir(parents=True,exist_ok=True)
  raw=baseline_bytes(specrow['path'],baseline_dir)
  if SHA(raw)!=specrow['file_sha256']:raise AssertionError('Baseline specification mismatch')
  src.write_bytes(raw)
  old=load_module('cec_baseline_architecture',legacyroot/'catholic-ai-pilot/_tools/agent_team.py')
  with patch.object(socket.socket,'connect',side_effect=AssertionError('network denied')),patch('socket.create_connection',side_effect=AssertionError('network denied')):
   prior=old.run_demo(temporary/'old-demo')
   current=run_demo(temporary/'new-demo',spec=spec,protected_root=ROOT)
   assert normalized_run(prior)==normalized_run(current),'Changed full synthetic result/trace'
   checks.append('full-run-input-output-trace-equivalence')
   assert len(current['events'])==10 and current['roles_before_pause']==4 and current['roles_after_resume']==5
   checks.append('five-role-order-and-pause-boundary')
   for variant in ['budget','role-error','packet-change','repeated-start']:
    records=[]
    for which in ['old','new']:
     kwargs={'max_calls':3} if variant=='budget' else {}
     team=(old.OfflineAgentTeam(temporary/f'{variant}-{which}',**kwargs) if which=='old'
           else OfflineAgentTeam(temporary/f'{variant}-{which}',spec=spec,protected_root=ROOT,**kwargs))
     if variant=='role-error':
      def fail(*args):raise RuntimeError('invented failure for equivalence check')
      team._fixture_response=fail
     if variant=='packet-change':team.packet['question']='changed after freeze'
     exception=None
     try:
      team.start()
      if variant=='repeated-start':team.start()
     except Exception as exc:exception=(type(exc).__name__,str(exc))
     assert exception is not None,variant+' did not fail'
     events=team.events() if (team.run_dir/'events.jsonl').exists() else []
     records.append((exception,normalized_events(events),team.execution_order))
    assert records[0]==records[1],variant+' baseline behavior changed'
    checks.append('baseline-equivalence-'+variant)
   team=OfflineAgentTeam(temporary/'guards',spec=spec,protected_root=ROOT)
   for name in ['shell.exec','github.merge','web.fetch','legiscan.write','send_email']:
    try:team.authorize_tool(name)
    except ValueError:pass
    else:raise AssertionError('Permission widened: '+name)
   checks.append('forbidden-operations-rejected')
   try:OfflineAgentTeam(ROOT/'catholic-ai-pilot/_evidence/forbidden',spec=spec,protected_root=ROOT)
   except ValueError:pass
   else:raise AssertionError('Corpus write destination accepted')
   checks.append('repository-output-path-rejected')
   try:OfflineAgentTeam(temporary/'live',spec=spec,protected_root=ROOT,mode='live')
   except ValueError:pass
   else:raise AssertionError('Live execution enabled')
   checks.append('live-mode-rejected')
   team.start()
   try:team.resume_fixture({'human_approved':True})
   except ValueError:pass
   else:raise AssertionError('Fabricated approval accepted')
   team.resume_fixture()
   try:team.publication_decision()
   except ValueError:pass
   else:raise AssertionError('Publishing enabled')
   checks.append('human-approval-and-publication-remain-blocked')
 after={p.relative_to(ROOT).as_posix():SHA(p.read_bytes()) for p in (ROOT/'catholic-ai-pilot').rglob('*') if p.is_file() and p.suffix!='.pyc'}
 assert before==after,'Checks changed reading/evidence files'
 assert SHA((ROOT/'src/cec_agents/tracing.py').read_bytes())==layout['baseline_modules']['catholic-ai-pilot/_tools/prompt_trace.py']
 checks.append('trace-implementation-identical-bytes')
 provenance=json.loads((ROOT/'catholic-ai-pilot/_provenance/runtime-refactor.json').read_text())
 for rel,sha in provenance['protected_file_sha256'].items():assert SHA((ROOT/rel).read_bytes())==sha,rel
 checks.append('all-baseline-evidence-and-root-readers-unchanged')
 return {'kind':'engineering_refactor_validation','baseline_commit':BASE,'checks':checks,'checks_passed':len(checks),'package_path':str(location),'installed_wheel_required':expect_installed,'normalized_fields':provenance['normalization_scope'],'live_model_calls':0,'research_service_calls':0,'independent_research_validation':False,'original_40_master_cells_unchanged':True}

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--expect-installed-wheel',action='store_true')
 p.add_argument('--baseline-dir',type=Path,help='Optional exact validated snapshot for offline local development')
 p.add_argument('--output',type=Path)
 args=p.parse_args();report=compare(expect_installed=args.expect_installed_wheel,baseline_dir=args.baseline_dir)
 encoded=json.dumps(report,indent=2)+'\n';print(encoded)
 if args.output:
  path=args.output.resolve()
  if path==ROOT.resolve() or ROOT.resolve() in path.parents:raise ValueError('Validation reports must go outside the checkout; retain via CI artifacts')
  path.parent.mkdir(parents=True,exist_ok=True);path.write_text(encoded)
 return 0
if __name__=='__main__':raise SystemExit(main())
