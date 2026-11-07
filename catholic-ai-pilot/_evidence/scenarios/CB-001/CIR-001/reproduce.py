#!/usr/bin/env python3
"""Rebuild frozen inputs and byte-equivalent procedure outputs in a new folder.

These are labelled replay copies, not new observations. No network or model
calls. The first-run receipt remains unchanged. Run from any directory.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, subprocess, sys
R=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
out=args.output.resolve()
if out.exists():raise FileExistsError('Use a new output directory; evidence is never overwritten.')
plan=json.loads((R/'plan.json').read_text())
receipt=json.loads((R/'execution.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if sha(R/'plan.json')!='202a69cb2d1fa7e6c944f6e4fd5a189d5ae90162e64296edf578360fdbb2bd37':raise ValueError('Plan differs from freeze')
if sha(R/'engine.py')!=plan['input_sha256']['engine.py']:raise ValueError('Engine differs from freeze')
legacy=R.parents[2]/'runs/SV-20261106-001/capture.json'
subprocess.run([sys.executable,str(R/'prepare_inputs.py'),'--output',str(out),'--legacy',str(legacy)],check=True)
spec=importlib.util.spec_from_file_location('gate_engine',R/'engine.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
cases=json.loads((out/'cases.json').read_text());registry=json.loads((out/'registry.json').read_text())
raw=[]
for c in cases:
    inputs={k:c[k] for k in ['target','selected','search_results','fetched','claim']}
    for name in ['locator_diagnostic','simple_checklist','structured_gate']:
        fn=getattr(m,name);result=fn(inputs) if name=='locator_diagnostic' else fn(inputs,registry)
        raw.append({'case_id':c['case_id'],'origin':c['origin'],'procedure':name,'output':result})
path=out/'raw-results.replay.json';path.write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n')
if sha(path)!=receipt['raw_results_sha256']:raise ValueError('Replay differs from first-run digest')
assert len(raw)==72 and all(r['output']['semantic_support']=='unreviewed' and r['output']['answer_verified'] is False for r in raw)
lines=['case_id,origin,reference_identity_admission,locator_diagnostic,simple_checklist,structured_gate']
for c in cases:
    o={r['procedure']:r['output']['status'] for r in raw if r['case_id']==c['case_id']}
    lines.append(','.join([c['case_id'],c['origin'],str(c['reference_identity_admission'])]+[o[n] for n in ['locator_diagnostic','simple_checklist','structured_gate']]))
(out/'case-results.csv').write_text('\n'.join(lines)+'\n')
summary={'kind':'content_equivalent_replay','source_run':receipt['run_id'],'outputs':len(raw),'raw_sha256':sha(path),'original_outputs_match':True,'new_live_observations':0,'independent_validation':False}
(out/'replay-receipt.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
