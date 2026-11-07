#!/usr/bin/env python3
"""One-time Catholic pilot consolidation. No research/network calls.
Run in a disposable checkout. Older reading editions remain in Git history.
"""
from pathlib import Path
import ast, copy, hashlib, json, re, shutil, sys
import nbformat
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
EXT='research/extensions/catholic-institutions'
E=ROOT/EXT; B=ROOT/'catholic-ai-pilot'; D=B/'_evidence'; P=B/'_provenance'; T=B/'_tools'
BASE='2ceb343b627b4aa13e3e5df84c4f7e8b2389683f'
URL='https://github.com/node-and-norm/control-evidence-corpus'
MASTER='reading/editions/0.4.4-draft/NodeNorm_Notebook_v0_4_4.ipynb'
MASTER_HASH='f72af7390066e4ac96b496351806c30bcb8d6c6757876551fa6d9370a2f18454'
sha=lambda b:hashlib.sha256(b).hexdigest()
text=lambda c:''.join(c['source']) if isinstance(c['source'],list) else c['source']
def save(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def md(s,kind='maintenance'):
 return nbformat.v4.new_markdown_cell(s,id='n-'+sha(s.encode())[:18],metadata={'node_norm':{'kind':kind,'new_research_results':False}})
def path_record(p):
 data=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(data),'bytes':len(data)}
assert E.is_dir() and not D.exists(),'Use the unmodified pre-consolidation snapshot.'
master_bytes=(E/MASTER).read_bytes();assert sha(master_bytes)==MASTER_HASH
old_files={p.relative_to(ROOT).as_posix():p.read_bytes() for p in E.rglob('*') if p.is_file()}
root_readme=(ROOT/'README.md').read_bytes()
manifest=json.loads((P/'book-manifest.json').read_text());study=json.loads((E/'study.json').read_text())
master=nbformat.reads(master_bytes.decode(),as_version=4)
original_raw=json.loads(master_bytes)['cells']
chapters={p.name:nbformat.read(p,as_version=4) for p in sorted(B.glob('*.ipynb'))}
relocated={};unique={};evidence_rows=[];alias_rows=[]
def retain(rel,dest=None):
 old=E/rel;target=D/(dest or rel);data=old.read_bytes();h=sha(data)
 if h in unique:
  final=unique[h];alias_rows.append({'old_path':old.relative_to(ROOT).as_posix(),'canonical_path':final,'sha256':h})
 else:
  target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
  final=target.relative_to(ROOT).as_posix();unique[h]=final
  evidence_rows.append({'old_path':old.relative_to(ROOT).as_posix(),**path_record(target),'relocation':'byte_identical'})
 relocated[old.relative_to(ROOT).as_posix()]=final
 return final
retain('study.json','design/study.json')
retain('archive/v0.2/study.json','design/original-study.json')
for p in sorted(E.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(E).as_posix()
 if rel.startswith(('data/','disclosure/','runs/','scenario-batches/')) and p.suffix in {'.json','.csv'}:
  retain(rel,rel.replace('data/','sources/',1) if rel.startswith('data/') else rel.replace('scenario-batches/','scenarios/',1))
 elif rel.startswith('evidence-workbench/') and p.suffix in {'.json','.csv'}:
  retain(rel,rel.replace('evidence-workbench/','methods/',1))
 elif rel.startswith('reading/archive-support/cir001/') and p.suffix in {'.json','.csv'}:
  retain(rel,rel.replace('reading/archive-support/cir001/','scenarios/CB-001/CIR-001/',1))
for rel in ['scenario-batches/CB-001/CIR-001/engine.py','scenario-batches/CB-001/CIR-001/prepare_inputs.py','scenario-batches/CB-001/CIR-001/reproduce.py','scenario-batches/CB-001/obligations/validate.py','scenario-batches/CB-001/PARISH-QA-001-R1/reproduce.py']:
 retain(rel,rel.replace('scenario-batches/','scenarios/',1))
T.mkdir(exist_ok=True)
(T/'check_evidence.py').write_bytes((E/'evidence-workbench/scripts/check_evidence.py').read_bytes())
def extract_function(file,name):
 s=(E/file).read_text();node=next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name==name)
 return ast.get_source_segment(s,node)+'\n'
(T/'capture_checks.py').write_text('"""Preserved source-capture checks; no live requests."""\nimport json,hashlib\n'+extract_function('scripts/build_release.py','derive'))
(T/'disclosure_checks.py').write_text('"""Preserved AI-disclosure checks; no approval inferred."""\nVERSION="0.1.0"\n'+extract_function('scripts/apply_ai_disclosure.py','validate_record'))
retired_navigation={EXT+'/'+r for r in ['README.md','reading/README.md','EVIDENCE_INDEX.md','RELEASE_NOTES.md','reading/ARCHIVE_POLICY.md','reading/NodeNorm_Protocol_v0_3_0.md','reading/NodeNorm_Protocol_v0_4_1.md','scenario-batches/CB-001/PARISH-QA-001-R1/READERS.md','evidence-workbench/README.md','evidence-workbench/course-alignment/README.md']}
source_map={x['source']:x['chapter'] for x in manifest['source_documents']}
def link_target(old):
 if old in relocated:return URL+'/blob/main/'+relocated[old]
 if old in source_map:return URL+'/blob/main/catholic-ai-pilot/'+source_map[old]
 return URL+'/blob/'+BASE+'/'+old

def fix_visible(s,where):
 for old,new in sorted(relocated.items(),key=lambda kv:-len(kv[0])):
  s=s.replace(URL+'/blob/main/'+old,URL+'/blob/main/'+new)
 def relative(m):
  label,dest=m.groups()
  if '://' in dest or dest.startswith(('#','mailto:','attachment:')):return m.group(0)
  raw=dest.split('#')[0].split('?')[0];p=(where.parent/raw).resolve()
  if not p.is_relative_to(ROOT):return m.group(0)
  rel=p.relative_to(ROOT).as_posix()
  if rel.startswith(EXT+'/'):return '['+label+']('+link_target(rel)+')'
  return m.group(0)
 return re.sub(r'(?<!!)\[([^\]\n]+)\]\(([^)\n]+)\)',relative,s)
for name,nb in chapters.items():
 kept=[];last_boundary=None
 for c in nb.cells:
  meta=c.metadata.get('node_norm',{})
  if meta.get('kind')=='source_boundary':last_boundary=c;continue
  if meta.get('kind')=='source_text':
   if meta.get('source_path') in retired_navigation:last_boundary=None;continue
   if last_boundary is not None:kept.append(last_boundary);last_boundary=None
  elif last_boundary is not None:kept.append(last_boundary);last_boundary=None
  if c.cell_type=='code':
   s=text(c).replace("'research/extensions/catholic-institutions'","'catholic-ai-pilot/_evidence'")
   s=s.replace('scenario-batches/','scenarios/').replace('reading/archive-support/cir001/replay-inputs/','scenarios/CB-001/CIR-001/replay-inputs/')
   s=s.replace("if not item['path'].endswith('.json'):","if not item.get('current_path', item['path']).endswith('.json'):")
   s=s.replace("(ROOT / item['path']).read_bytes()","(ROOT / item.get('current_path',item['path'])).read_bytes()")
   c.source=s;c.execution_count=None;c.outputs=[]
  else:c.source=fix_visible(text(c),B/name)
  kept.append(c)
 nb.cells=kept
 nb.metadata['node_norm']['maintenance_edition']='1.1.0-consolidation'
 nb.metadata['node_norm']['source_storage']='notebook_native; evidence in _evidence; history in Git'
flow=study['pipeline']
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 390" role="img" aria-labelledby="title desc"><title id="title">Six-stage research workflow</title><desc id="desc">Discover, Screen, Review, Reconstruct, Evaluate, Report. Planning sequence, not completed stages.</desc><rect width="1080" height="390" rx="18" fill="#f7f6f3"/>']
short=[['Sources and candidate risks','Retain source identities'],['Institutional relevance','Keep exclusion reasons'],['Qualified judgments','Record disagreements'],['Control opportunities','Retain missing evidence'],['Frozen comparisons','Keep failed trials'],['Bounded findings','Disclose review status']]
for i,row in enumerate(flow):
 x=22+(i%3)*356;y=25+(i//3)*165
 svg += [f'<rect x="{x}" y="{y}" width="324" height="140" rx="12" fill="white" stroke="#d7d1e7"/><text x="{x+18}" y="{y+28}" font-family="Arial,sans-serif" font-size="15" fill="#5145cd">{row["number"]}</text><text x="{x+18}" y="{y+62}" font-family="Arial,sans-serif" font-size="23" font-weight="bold" fill="#1c1923">{row["title"]}</text><text x="{x+18}" y="{y+92}" font-family="Arial,sans-serif" font-size="15" fill="#5f5b67">{short[i][0]}</text><text x="{x+18}" y="{y+116}" font-family="Arial,sans-serif" font-size="14" fill="#5f5b67">{short[i][1]}</text>']
svg.append('<text x="25" y="370" font-family="Arial,sans-serif" font-size="14" fill="#5f5b67">Planning sequence only. Research completion and independent review require separate evidence.</text></svg>')
(B/'assets/workflow.svg').write_text(''.join(svg))
workflow='## The six-step research workflow\n\n![Discover, Screen, Review, Reconstruct, Evaluate, Report](assets/workflow.svg)\n\n**01 Discover → 02 Screen → 03 Review → 04 Reconstruct → 05 Evaluate → 06 Report.**\n\nThis describes the planned research process. It does not assert that every stage is complete. The citation comparison and six collected responses are early development evidence; qualified source interpretation and institutional effectiveness remain open.\n\n'
workflow+='| Step | Work and required record |\n| :--- | :--- |\n'+'\n'.join('| '+r['number']+' '+r['title']+' | '+r['description'].replace('|','\\|')+' |' for r in flow)
roadmap='## The seven-stage milestone plan\n\n**Retained planning snapshot:** status labels are historical, not newly awarded approvals. The six-step workflow describes the process; these seven milestones describe its planning gates.\n\n| Stage | Milestone | Recorded state | Evidence gate |\n| :--- | :--- | :--- | :--- |\n'+'\n'.join('| '+r['n']+' | '+r['name']+' | '+r['state'].replace('_',' ')+' | '+r['gate'].replace('|','\\|')+' |' for r in study['stages'])
nb=chapters['01_Study_and_Roadmap.ipynb']
nb.cells=[c for c in nb.cells if not text(c).startswith('## Original seven-stage roadmap')]
nb.cells[2:2]=[md(workflow),md(roadmap)]
guide='''# Catholic institutional AI pilot: complete study

**The complete 0.4.4 reading notebook is now at the repository root.** This consolidated reading entry retains all its original cells, embedded inputs, saved outputs and research limits. The earlier version labels inside it identify historical checkpoints; relocation is not a new experiment or approval.

[Chapter index](catholic-ai-pilot/00_START_HERE.ipynb) · [Visual workflow and roadmap](catholic-ai-pilot/01_Study_and_Roadmap.ipynb) · [Protocol](catholic-ai-pilot/02_Research_Protocol.ipynb) · [Results](catholic-ai-pilot/03_Citation_Test_Results.ipynb) · [AI disclosure](catholic-ai-pilot/07_AI_Disclosure.ipynb)

**Read without running code.** The stored outputs are available in this notebook. Optional execution replays local calculations using embedded records; it makes no new research service calls. The other chapters provide focused routes into the same study, rather than additional versions of the entire report.

**Current research boundary:** one constructed citation comparison and six collected service responses. Qualified interpretation, independent review and institutional safeguard effectiveness remain unresolved. No canonical approval or compliance conclusion is supplied.

**Version custody:** old reading editions are preserved at earlier Git commits and existing releases, outside the current checkout. No duplicate archive directory is needed. Historical instructions inside retained cells are records of that earlier build, not directions for the current checkout. Current maintenance instructions are in [Reproduce and inspect](catholic-ai-pilot/09_Reproduce_and_Inspect.ipynb).
'''
master_original_cells=copy.deepcopy(master.cells)
master.cells=[md(guide),md(workflow.replace('(assets/','(catholic-ai-pilot/assets/'))]+master.cells
master.metadata['consolidation']={'source_commit':BASE,'original_path':EXT+'/'+MASTER,'original_sha256':MASTER_HASH,'original_cells_unchanged':True,'original_cell_count':len(master_original_cells),'new_research_results':False,'qualified_review':'pending'}
nbformat.write(master,ROOT/'CATHOLIC_PILOT.ipynb')
cir=json.loads((D/'scenarios/CB-001/CIR-001/ai-use-and-publication.json').read_text())
def pretty(x):
 if isinstance(x,dict):return '\n\n'.join('**'+k.replace('_',' ')+'**\n\n'+pretty(v) for k,v in x.items())
 if isinstance(x,list):return '\n'.join('- '+pretty(v) for v in x) if x else '*No entries recorded.*'
 if x is None:return '*Not recorded (null).*'
 return str(x)
disclosure='## CIR-001: complete run-level AI disclosure\n\nThis is the retained record, not a new attestation.\n\n'+pretty(cir)
chapters['07_AI_Disclosure.ipynb'].cells.insert(2,md(disclosure,'record_projection'))
chapters['07_AI_Disclosure.ipynb'].cells.insert(2,md('''## Disclosure coverage

| Activity | Inspect here | Boundary |
| :--- | :--- | :--- |
| Study design, source work, code and drafting | Full study disclosure and contribution record below | Authorization is not source verification. |
| Citation engineering comparison | Complete CIR-001 AI-use record below | The same assistant authored the engine and reference cases. |
| Canonical applicability proposals | [Canon-law chapter](04_Canon_Law_and_Authority.ipynb) and retained decision record | Qualified review remains pending. |
| Six external service responses | [Exact responses and capture limits](05_Live_Parish_Responses.ipynb) | Magisterium supplied outputs; this is not an independent AI panel. |
| Repository consolidation | Maintenance record in `_provenance/consolidation.json` | One assistant reorganized files and ran software checks; no new research or human approval. |

Unknown model snapshots and missing historical capture remain unknown. Historical publisher guidance is preserved as dated guidance, not a current universal compliance certificate.
'''))
chapters['09_Reproduce_and_Inspect.ipynb'].cells=[md('''# 09. Reproduce and inspect

[Contents](00_START_HERE.ipynb) · [Previous: Decisions and review](08_Decisions_and_Review.ipynb) · [Next: Evidence methods](10_Evidence_Methods.ipynb)

## One current study, one evidence collection

The [complete study](../CATHOLIC_PILOT.ipynb) is the front door. Numbered notebooks are focused reading chapters. `_evidence/` contains the retained machine records and replay code. `_provenance/` records their original locations, byte hashes, source commitments and the consolidation decision. There is no second reader archive in the current download.

The notebook cells are now the maintained reading source. The retired fixed-commit builders must not be used to overwrite them. A change to evidence requires a new run or explicit correction and a corresponding notebook/provenance update. Checks fail when retained evidence no longer matches its recorded hash.

## Read first; run only when needed

GitHub's notebook preview displays text and saved output. Clone or download the current repository to execute optional checks. The complete root notebook is self-contained. The three short chapter checks require the repository's `_evidence` collection. None calls a model or research service.

```bash
python -m pip install -r requirements.txt -r catholic-ai-pilot/requirements.txt
python scripts/check_catholic_pilot.py
python scripts/check_catholic_pilot.py --execute
python -m unittest discover -s tests -v
```

The execution command uses temporary copies, preserving saved outputs. Replaying stored data is different from reissuing prompts to a service. A live replication requires a new plan and retained responses.

## Inspect the earlier runs

```bash
python catholic-ai-pilot/_evidence/scenarios/CB-001/CIR-001/reproduce.py --output /tmp/cir-replay-new
python catholic-ai-pilot/_evidence/scenarios/CB-001/PARISH-QA-001-R1/reproduce.py
python catholic-ai-pilot/_evidence/scenarios/CB-001/obligations/validate.py
python catholic-ai-pilot/_tools/check_evidence.py
```

Use a new output directory for each citation replay. The frozen engine, preparation recipe, original result digest, captured responses and canonical pending states were preserved. Replay output remains a replay, not a new observation or independent validation.

## Recover older editions without duplicating the checkout

The exact pre-cleanup repository is available at [commit 2ceb343](https://github.com/node-and-norm/control-evidence-corpus/tree/2ceb343b627b4aa13e3e5df84c4f7e8b2389683f). Earlier delivered editions remain in that history; the published 0.4.1 development release is unchanged. A current source ZIP contains only the current tree. A normal full Git clone also carries historical objects, although older files do not appear in its current working folders.

Commit-pinned historical links remain historical. Old links that explicitly use `main` and a retired path can stop resolving; use the root study link for current reading, and the recorded commit for historical citations. We deliberately avoid duplicate files or a second legacy directory merely to simulate redirects.

## What the checks do and do not establish

Checks cover notebook format, local navigation, retained source text, evidence identity, the 24-packet replay and the six-response inventory. They do not establish source truth, qualified reviewer competence, doctrinal correctness, canonical applicability or institutional effectiveness.

[AI disclosure](07_AI_Disclosure.ipynb) and [Decisions and review](08_Decisions_and_Review.ipynb) identify unresolved review. No approval is inferred from a successful build.
''')]
chapters['00_START_HERE.ipynb'].cells.insert(1,md('## Read the complete workbook first\n\n[Open the complete study notebook at the repository root](../CATHOLIC_PILOT.ipynb). It contains the original six-stage workflow, roadmap, recorded results and embedded evidence. Use the chapters below for a focused review. Older full-report versions remain in Git history instead of duplicate archive folders.'))
for c in chapters['00_START_HERE.ipynb'].cells:
 if text(c).startswith('## Reading, archives and disclosure'):
  c.source='## Reading, history and disclosure\n\nThe current reading path is notebooks only. The supporting records are stored once under `_evidence`. Earlier versions remain in Git history and existing releases rather than a duplicate archive in a fresh download. [Reproduce and inspect](09_Reproduce_and_Inspect.ipynb) explains the relationship. This cleanup adds no research results or review judgments. [AI disclosure](07_AI_Disclosure.ipynb).'
chapters['08_Decisions_and_Review.ipynb'].cells.insert(2,md('''## Consolidation decision

The maintainer requested the complete study workbook upfront and no duplicate historical reader files in current downloads. The complete 0.4.4 notebook was promoted to the repository root. The six-stage workflow was restored at the front. Unique evidence and run code were relocated without changing their bytes. Superseded reading editions, redundant document navigation and obsolete export builders were removed from the working tree; Git history and releases retain their original versions.

This maintenance did not repeat research requests, change prior outcomes, supply a new theological judgment or fill a human-review attestation. Source and software checks are separate from scientific validation. The exact move/removal ledger and AI maintenance disclosure are in `_provenance/consolidation.json`.
'''))
for name,nb in chapters.items():nbformat.validate(nb);nbformat.write(nb,B/name)
manifest['source_documents']=[r for r in manifest['source_documents'] if r['source'] not in retired_navigation]
manifest['inputs']=[dict(r,current_path=relocated[r['path']]) for r in manifest['inputs'] if r['path'] in relocated]
manifest['maintenance_edition']='1.1.0-consolidation'
manifest['current_source']='native_notebooks_with_hash_verified_evidence'
manifest['source_mode']='git_commit'
manifest['root_entry']='CATHOLIC_PILOT.ipynb'
save(P/'book-manifest.json',manifest)
(P/'validation.json').unlink(missing_ok=True);(P/'maintenance-disclosure.json').unlink(missing_ok=True)
for name,newname in [('test_ai_disclosure.py','test_catholic_disclosure_record.py'),('test_release.py','test_catholic_source_capture.py')]:
 s=(E/'scripts'/name).read_text()
 if name=='test_ai_disclosure.py':
  s=s.replace("ROOT=Path(__file__).resolve().parent.parent","ROOT=Path(__file__).resolve().parents[1]/'catholic-ai-pilot'\nE=ROOT/'_evidence'")
  s=s.replace("ROOT/'scripts/apply_ai_disclosure.py'","ROOT/'_tools/disclosure_checks.py'").replace("ROOT/'disclosure/","E/'disclosure/")
  removed={'test_idempotent_html','test_deterministic_statement'}
 else:
  s=s.replace("ROOT=Path(__file__).resolve().parent.parent","ROOT=Path(__file__).resolve().parents[1]/'catholic-ai-pilot'\nE=ROOT/'_evidence'")
  s=s.replace("ROOT/'scripts/build_release.py'","ROOT/'_tools/capture_checks.py'").replace("ROOT/'runs/","E/'runs/")
  s=s.replace("(ROOT/'data/normative-crosswalk.json').read_bytes(),(ROOT/'archive/v0.2/data/normative-crosswalk.json').read_bytes()","hashlib.sha256((E/'sources/normative-crosswalk.json').read_bytes()).hexdigest(),'d9d76d58dc0186e1a5956b66028992845ef5f1b273d3ca1eccdb4f5fa24bf5d0'")
  s=s.replace("ROOT/'study.json'","E/'design/study.json'").replace("ROOT/'archive/v0.2/study.json'","E/'design/original-study.json'")
  removed={'test_five_reading_files','test_main_readme_unchanged'}
 tree=ast.parse(s);lines=s.splitlines(keepends=True)
 intervals=[(n.lineno-1,n.end_lineno) for cl in tree.body if isinstance(cl,ast.ClassDef) for n in cl.body if isinstance(n,ast.FunctionDef) and n.name in removed]
 for a,b in sorted(intervals,reverse=True):del lines[a:b]
 (ROOT/'tests'/newname).write_text(''.join(lines))
for p in (ROOT/'tests').glob('test_catholic_*.py'):
 if p.name in {'test_catholic_reader_archive.py','test_catholic_protocol_notebook.py','test_catholic_book_visible_text.py','test_catholic_notebook_book.py'}:
  p.unlink();continue
 s=p.read_text().replace(EXT+'/scenario-batches/','catholic-ai-pilot/_evidence/scenarios/');p.write_text(s)
for p in [ROOT/'docs/README.md',ROOT/'docs/policies/AI_USE_POLICY.md']:
 s=p.read_text().replace('../research/extensions/catholic-institutions/README.md','../CATHOLIC_PILOT.ipynb')
 s=s.replace('../../research/extensions/catholic-institutions/disclosure/README.md','../../catholic-ai-pilot/07_AI_Disclosure.ipynb');p.write_text(s)
retired_workflows=['catholic-study.yml','catholic-reader-archive.yml','catholic-protocol-notebook.yml','catholic-notebook-book.yml']
for name in retired_workflows:(ROOT/'.github/workflows'/name).unlink(missing_ok=True)
for name in ['build_catholic_notebook_book.py','check_catholic_notebook_book.py']:(ROOT/'scripts'/name).unlink(missing_ok=True)
shutil.rmtree(E)
(B/'requirements.txt').write_text('nbformat==5.10.4\nnbclient==0.10.4\nipykernel==7.2.0\n')
retired=[{'old_path':p,'sha256':sha(data),'bytes':len(data),'preserved_at_commit':BASE,'reason':'superseded reader, historical edition or retired presentation builder; retained in Git history'} for p,data in old_files.items() if p not in relocated]
ledger={'kind':'working_tree_consolidation','baseline_commit':BASE,'research_status':'unchanged; exploratory; qualified review pending','new_research_results':False,'new_model_or_service_calls':0,'history_rewritten':False,'old_directory_removed':EXT,'root_complete_notebook':{'path':'CATHOLIC_PILOT.ipynb','source_path':EXT+'/'+MASTER,'source_sha256':MASTER_HASH,'original_cells':len(master_original_cells),'original_cell_source_hashes':[sha(text(c).encode()) for c in master_original_cells],'original_code_outputs':[{'cell_id':c['id'],'execution_count':c['execution_count'],'outputs_sha256':sha(json.dumps(c['outputs'],sort_keys=True,ensure_ascii=False).encode())} for c in original_raw if c['cell_type']=='code']},'retained_evidence':evidence_rows,'identical_aliases':alias_rows,'retired_files':retired,'retired_navigation_sources':sorted(retired_navigation),'retired_workflows':retired_workflows,'replacement_tests':'frozen run checks, disclosure/capture mutation checks, source reassembly, checksums, navigation and notebook execution','ai_assistance':{'system':'ChatGPT','exact_provider_snapshot':None,'contributions':['dependency audit','file relocation','notebook navigation and visual restoration','test migration','software validation'],'human_authorization':'explicit maintainer request','personal_source_verification':'not_recorded','independent_review':'not_performed','qualified_canonical_review':'pending'},'root_readme_sha256':sha(root_readme),'maintenance_attempts':[{'stage':'local output-hash validation','outcome':'first attempt failed because nbformat normalized multiline output fields before hashing; fixed by deriving output hashes from the original JSON serialization; original cell objects remained identical'},{'stage':'local complete repository tests','outcome':'Python 3.13 source-ZIP environment: 64 Catholic tests passed; unrelated general tests lacked Git metadata and two numeric comparisons differed. Full Python 3.11 Git checkout CI is required before merge.'}]}
save(P/'consolidation.json',ledger)
assert (ROOT/'README.md').read_bytes()==root_readme
from nbclient import NotebookClient
for p in sorted(B.glob('*.ipynb')):
 n=nbformat.read(p,as_version=4)
 if any(c.cell_type=='code' for c in n.cells):
  NotebookClient(n,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute();nbformat.write(n,p)
# The original complete notebook's inherited cells must remain semantically and structurally exact.
assert json.loads((ROOT/'CATHOLIC_PILOT.ipynb').read_text())['cells'][2:]==original_raw
# Retain this one-time migration in Git history, not as a competing active builder.
(ROOT/'scripts/consolidate_catholic_pilot.py').unlink(missing_ok=True)
(ROOT/'.github/workflows/catholic-consolidation.yml').unlink(missing_ok=True)
print(json.dumps({'old_extension_files':len(old_files),'retained_evidence_files':len(evidence_rows),'identical_aliases':len(alias_rows),'old_paths_removed':len(old_files),'retired_reader_and_builder_files':len(retired),'master_original_cells':len(master_original_cells),'notebook_chapters':len(chapters)},indent=2))
