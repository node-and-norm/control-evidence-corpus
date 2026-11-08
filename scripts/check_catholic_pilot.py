#!/usr/bin/env python3
"""Current Catholic notebook/evidence custody checks. No research/API calls.
--execute replays temporary notebook copies; it never rewrites saved outputs.
"""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote,urlsplit
import argparse,copy,hashlib,json,re,runpy,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'catholic-ai-pilot'
sha=lambda x:hashlib.sha256(x).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def text(c):return ''.join(c['source']) if isinstance(c['source'],list) else c['source']
def check(root:Path=ROOT)->dict:
 b=root/'catholic-ai-pilot';ledger=load(b/'_provenance/consolidation.json');manifest=load(b/'_provenance/book-manifest.json')
 assert not (root/'research/extensions/catholic-institutions').exists(),'Legacy workspace remains'
 assert not any(p.name.lower() in {'archive','_archive','editions','reading'} for p in b.rglob('*') if p.is_dir()),'Duplicate reader archive remains'
 assert not any(p.suffix.lower() in {'.md','.html','.pdf'} for p in b.rglob('*') if p.is_file()),'Non-notebook reader present'
 assert sha((root/'README.md').read_bytes())==ledger['root_readme_sha256'],'Root README changed'
 assert not ledger['history_rewritten'] and not ledger['new_research_results']
 for r in ledger['retained_evidence']:
  p=(root/r['path']).resolve();assert p.is_relative_to(root.resolve())
  data=p.read_bytes();assert len(data)==r['bytes'] and sha(data)==r['sha256'],r['path']
 pages=[root/'CATHOLIC_PILOT.ipynb']+[root/r['path'] for r in manifest['chapters']]
 assert len(pages)==18 and len(set(pages))==18
 links=0;source=defaultdict(list);code_count=0
 for p in pages:
  n=load(p);assert n['nbformat']==4
  ids=[c['id'] for c in n['cells']];assert len(ids)==len(set(ids))
  for c in n['cells']:
   s=text(c)
   if c['cell_type']=='code':
    code_count+=1;assert c['execution_count'] is not None
    assert not any(o['output_type']=='error' for o in c['outputs'])
    if p!=pages[0]:assert "'research/extensions/catholic-institutions'" not in s
   if c['cell_type']=='markdown':
    for target in re.findall(r'!?\[[^\]]*\]\(([^)\n]+)\)',s):
     u=urlsplit(target)
     if u.scheme or target.startswith(('#','attachment:')):continue
     path=unquote(u.path)
     if not path:continue
     dest=(p.parent/path).resolve();assert dest.is_relative_to(root.resolve()),target
     assert dest.exists(),f'{p.name}: {target}'
     assert dest.suffix not in {'.md','.html','.pdf'},target
     links+=1
   m=c.get('metadata',{}).get('node_norm',{})
   if m.get('kind')=='source_text':source[m['source_path']].append((m['section'],m['original_text']))
 expected={r['source']:r for r in manifest['source_documents']}
 assert set(source)==set(expected),(set(source)-set(expected),set(expected)-set(source))
 assert len(source)>=20
 for path,parts in source.items():assert sha(''.join(s for _,s in sorted(parts)).encode())==expected[path]['sha256'],path
 complete=load(pages[0]);original=complete['cells'][2:]
 saved=ledger['root_complete_notebook'];assert len(original)==saved['original_cells']==40
 assert [sha(text(c).encode()) for c in original]==saved['original_cell_source_hashes']
 for r in saved['original_code_outputs']:
  c=next(c for c in original if c['id']==r['cell_id'])
  assert c['execution_count']==r['execution_count'] and sha(json.dumps(c['outputs'],sort_keys=True,ensure_ascii=False).encode())==r['outputs_sha256']
 evidence=load(b/'_evidence/scenarios/CB-001/PARISH-QA-001-R1/evidence.json')
 visible='\n'.join(text(c) for c in load(b/'05_Live_Parish_Responses.ipynb')['cells'] if c['cell_type']=='markdown')
 for r in evidence['records']:
  assert r['prompt'] in visible and r['response']['answer'] in visible
 assert len(evidence['records'])==6
 discourse='\n'.join(text(c) for c in load(b/'07_AI_Disclosure.ipynb')['cells'])
 assert 'AIU-CIR001-R1' in discourse and 'same assistant' in discourse.lower()
 assert (b/'assets/workflow.svg').exists()
 assert 'assets/workflow.svg' in '\n'.join(text(c) for c in load(b/'01_Study_and_Roadmap.ipynb')['cells'])
 for fn in ['catholic-study.yml','catholic-reader-archive.yml','catholic-protocol-notebook.yml','catholic-notebook-book.yml']:
  assert not (root/'.github/workflows'/fn).exists(),fn
 return {'kind':'software_and_custody_validation','notebooks':len(pages),'original_master_cells_preserved':40,
         'retained_source_documents':len(source),'byte_identical_evidence_files':len(ledger['retained_evidence']),
         'local_reader_links':links,'stored_code_cells':code_count,'exact_service_responses':6,
         'duplicate_archive_directories':0,'legacy_workspace_removed':True,
         'new_research_calls':0,'independent_research_validation':False}

def execute(root:Path=ROOT)->list[dict]:
 import nbformat
 from nbclient import NotebookClient
 b=root/'catholic-ai-pilot';pages=[root/'CATHOLIC_PILOT.ipynb']+[p for p in sorted(b.glob('*.ipynb')) if any(c['cell_type']=='code' for c in load(p)['cells'])]
 rows=[]
 for p in pages:
  raw=p.read_bytes();n=nbformat.read(p,as_version=4)
  with tempfile.TemporaryDirectory() as d:
   work=d if p.name=='CATHOLIC_PILOT.ipynb' else str(root)
   NotebookClient(n,timeout=120,kernel_name='python3',resources={'metadata':{'path':work}}).execute()
  assert p.read_bytes()==raw
  rows.append({'path':p.relative_to(root).as_posix(),'code_cells':sum(c.cell_type=='code' for c in n.cells),'temporary_copy':True,'archive_outputs_unchanged':True,'new_research_calls':0})
 return rows

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');p.add_argument('--output',type=Path)
 a=p.parse_args();r=check()
 if a.execute:r['executions']=execute()
 s=json.dumps(r,indent=2)+'\n';print(s)
 if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
