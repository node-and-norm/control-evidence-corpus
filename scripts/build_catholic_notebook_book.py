#!/usr/bin/env python3
"""Import the preserved Catholic pilot into a top-level, notebook-only reading book.

The input commit is fixed. No research/API/model calls, no deletion of archives.
Generated narrative cells retain their original text in provenance metadata so
link retargeting can be checked without silently changing historical wording.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import posixpath
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit, unquote

BASE = 'c1628ae86186e2202ef82e1394f0b8bb8f7568ab'
EXT = 'research/extensions/catholic-institutions'
REPO_URL = 'https://github.com/node-and-norm/control-evidence-corpus'
BOOK = 'catholic-ai-pilot'
ENTRY = 'CATHOLIC_PILOT.ipynb'
VERSION = '1.0.0-navigation'
ROOT = Path(__file__).resolve().parents[1]
NAV = '\n<!-- catholic-notebook-book:start -->\n**Catholic institutional AI pilot:** [Open the guided notebook book](CATHOLIC_PILOT.ipynb) · [Browse its chapters](catholic-ai-pilot/00_START_HERE.ipynb).\n<!-- catholic-notebook-book:end -->\n'
CHAPTERS = [
 ('00_START_HERE.ipynb','Start here','Choose a reading path and understand the research status.'),
 ('01_Study_and_Roadmap.ipynb','Study and roadmap','The question, hypotheses, current findings and remaining work.'),
 ('02_Research_Protocol.ipynb','Research protocol','The complete protocol and recorded method amendment.'),
 ('03_Citation_Test_Results.ipynb','Citation-test results','The complete CIR-001 result, source packet, freeze and replay.'),
 ('04_Canon_Law_and_Authority.ipynb','Canon law and authority','Candidate obligations, source types and limits of applicability.'),
 ('05_Live_Parish_Responses.ipynb','Live parish-assistant responses','All six exact prompts, answers, references and recording limits.'),
 ('06_Risk_Scenarios_and_Sources.ipynb','Risk scenarios and sources','All five scenario drafts and their source records.'),
 ('07_AI_Disclosure.ipynb','AI assistance and responsibility','Contributions, actual human review and publication guidance.'),
 ('08_Decisions_and_Review.ipynb','Decisions and review','Decision history, disagreements, qualifications and review worksheet.'),
 ('09_Reproduce_and_Inspect.ipynb','Reproduce and inspect','Offline checks, source lineage, archived editions and reading history.'),
 ('10_Evidence_Methods.ipynb','Evidence methods','The full evidence-workbench review and documentation requirements.'),
 ('11_Course_and_Method_Alignment.ipynb','Course and method alignment','The full retained comparison with the research-course materials.'),
]
CIR = 'scenario-batches/CB-001/CIR-001/'
PQA = 'scenario-batches/CB-001/PARISH-QA-001-R1/'
OA = 'scenario-batches/CB-001/obligations/'
LINK_RE = re.compile(r'(?<!!)\[([^\]\n]+)\]\(([^)\n]+)\)')


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> bytes:
    return subprocess.check_output(['git', *args], cwd=ROOT)


class Sources:
    def __init__(self, working_copy: bool = False):
        self.working_copy = working_copy
        self.used: dict[str, dict] = {}
    def read(self, rel: str) -> bytes:
        full = f'{EXT}/{rel}'
        data = (ROOT/full).read_bytes() if self.working_copy else git('show', f'{BASE}:{full}')
        self.used[rel] = {'path':full, 'sha256':digest(data), 'bytes':len(data), 'source_commit':BASE}
        return data
    def text(self, rel: str) -> str:
        return self.read(rel).decode('utf-8')
    def obj(self, rel: str):
        return json.loads(self.read(rel))
    def markdowns(self) -> list[str]:
        if self.working_copy:
            paths = [str(p.relative_to(ROOT/EXT)) for p in (ROOT/EXT).rglob('*.md')]
        else:
            paths = [p.removeprefix(EXT+'/') for p in git('ls-tree','-r','--name-only',BASE,'--',EXT).decode().splitlines()]
        return sorted(p for p in paths if p.endswith('.md') and not p.startswith(('archive/','reading/editions/')))


def chapter_for(path: str) -> int:
    if path == 'SCOPING.md': return 1
    if path in {'PROTOCOL.md','METHOD_AMENDMENT.md'}: return 2
    if path.startswith(CIR): return 3
    if path.startswith(OA): return 4
    if path.startswith(PQA): return 8 if path.endswith('REVIEW.md') else 5
    if path == 'scenario-batches/CB-001/README.md': return 6
    if path in {'AI_DISCLOSURE.md','disclosure/README.md','evidence-workbench/AI_USE_DISCLOSURE.md'}: return 7
    if path in {'DECISIONS.md','CHANGELOG.md','DISCLOSURE_CHANGELOG.md'}: return 8
    if path.startswith('evidence-workbench/course-alignment/'): return 11
    if path.startswith('evidence-workbench/'): return 10
    return 9


def notebook(cells: list[dict], title: str) -> dict:
    return {'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
      'language_info':{'name':'python','version':'3.11'},
      'node_norm':{'book_version':VERSION,'source_commit':BASE,'title':title,
       'research_status':'exploratory; qualified review pending','main_protocol':'0.3.0; unfrozen',
       'new_research_results':False,'network_required_for_reading_or_checks':False}},'nbformat':4,'nbformat_minor':5}


def md(text: str, *, kind: str = 'editorial', **meta) -> dict:
    ident = digest((kind+json.dumps(meta,sort_keys=True)+text).encode())[:18]
    return {'cell_type':'markdown','id':'m-'+ident,'metadata':{'node_norm':{'kind':kind,**meta}},'source':text}


def code(text: str) -> dict:
    return {'cell_type':'code','id':'c-'+digest(text.encode())[:18],
      'metadata':{'node_norm':{'kind':'offline_record_check','not_new_research':True}},
      'source':text,'execution_count':None,'outputs':[]}


def words(key: str) -> str:
    return key.replace('_',' ').strip().capitalize()


def pretty(value, depth: int = 0) -> str:
    """Readable, lossless-value projection. Machine keys stay in source metadata."""
    if isinstance(value, dict):
        return '\n\n'.join('**'+words(str(k))+'**\n\n'+pretty(v,depth+1) for k,v in value.items())
    if isinstance(value, list):
        if not value: return '*No entries recorded.*'
        if all(not isinstance(v,(dict,list)) for v in value):
            return '\n'.join('- '+pretty(v,depth+1) for v in value)
        return '\n\n---\n\n'.join(pretty(v,depth+1) for v in value)
    if value is None: return '*Not recorded (null).*'
    if isinstance(value,bool): return '`'+str(value).lower()+'`'
    return str(value)


def retarget(text: str, source_path: str, mapping: dict[str,int]) -> str:
    def replace(match):
        label, target = match.groups()
        u = urlsplit(target)
        if target.startswith('#'): return match.group(0)
        if u.scheme:
            if not target.startswith(REPO_URL+'/'): return match.group(0)
            if '/'+EXT+'/' not in target:
                return '['+label+']('+CHAPTERS[9][0]+')' if u.path.endswith(('.md','.html','.pdf')) else match.group(0)
            path = target.split('/'+EXT+'/',1)[1].split('#',1)[0]
        else:
            path = posixpath.normpath(posixpath.join(posixpath.dirname(source_path),unquote(u.path)))
        if path in mapping:
            return '['+label+']('+CHAPTERS[mapping[path]][0]+')'
        if path.endswith(('.md','.html','.pdf')):
            return '['+label+']('+CHAPTERS[9][0]+')'
        if u.scheme: return match.group(0)
        if path.startswith('../'):
            full = posixpath.normpath(EXT+'/'+path)
        else:
            full = EXT+'/'+path
        return '['+label+']('+REPO_URL+'/blob/'+BASE+'/'+full+('?' + u.query if u.query else '')+('#'+u.fragment if u.fragment else '')+')'
    return LINK_RE.sub(replace,text)


def pieces(text: str) -> list[str]:
    starts=[0]; offset=0; fence=False
    for line in text.splitlines(keepends=True):
        if line.startswith('```'): fence=not fence
        if not fence and offset and re.match(r'^#{1,2} ',line): starts.append(offset)
        offset+=len(line)
    starts.append(len(text))
    return [text[a:b] for a,b in zip(starts,starts[1:]) if b>a]


def add_source(cells: list, rel: str, src: Sources, mapping: dict, coverage: list) -> None:
    text=src.text(rel)
    cells.append(md('---\n\n## Retained record: '+Path(rel).name+'\n\n'
      '> The following is the complete retained source record. Its dates and descriptions of earlier checkpoints remain historical. '
      'Link targets lead to the notebook chapters; the original text is preserved in cell provenance.\n\n'
      '**Source identifier:** `'+rel+'`',kind='source_boundary'))
    start=len(cells)
    for i,part in enumerate(pieces(text)):
        cells.append(md(retarget(part,rel,mapping),kind='source_text',source_path=EXT+'/'+rel,
          source_commit=BASE,section=i,source_sha256=digest(text.encode()),original_text=part))
    coverage.append({'source':EXT+'/'+rel,'chapter':CHAPTERS[chapter_for(rel)][0],
       'sha256':digest(text.encode()),'source_cells':len(cells)-start,'complete_text_preserved':True})


def add_json(cells: list, rel: str, src: Sources, title: str, items_key: str | None = None) -> None:
    value=src.obj(rel)
    cells.append(md('## '+title+'\n\n**Retained machine-readable source:** `'+rel+'`. '
       'The sections below display the stored values; they add no judgment or approval.',kind='source_boundary'))
    blocks=[value] if not items_key else [{k:v for k,v in value.items() if k!=items_key},*value[items_key]]
    for i,block in enumerate(blocks):
        cells.append(md(pretty(block),kind='record_projection',source_path=EXT+'/'+rel,
          source_commit=BASE,record=i,source_sha256=digest(src.read(rel))))


OFFLINE_ROOT = '''# Local record check only. No network or model calls.
from pathlib import Path
import json, hashlib
ROOT = next((p for p in [Path.cwd(), *Path.cwd().parents]
             if (p / 'research/extensions/catholic-institutions').is_dir()), None)
if ROOT is None:
    raise FileNotFoundError('Run from the checked-out repository or its catholic-ai-pilot folder.')
E = ROOT / 'research/extensions/catholic-institutions'
manifest = json.loads((ROOT / 'catholic-ai-pilot/_provenance/book-manifest.json').read_text())
for item in manifest['inputs']:
    if not item['path'].endswith('.json'):
        continue
    data = (ROOT / item['path']).read_bytes()
    if hashlib.sha256(data).hexdigest() != item['sha256']:
        raise ValueError('Source changed since the book snapshot: ' + item['path'])
'''


def navigation(i: int) -> str:
    links=['[Contents](00_START_HERE.ipynb)']
    if i>0: links.insert(0,'[Previous: '+CHAPTERS[i-1][1]+']('+CHAPTERS[i-1][0]+')')
    if i+1<len(CHAPTERS): links.append('[Next: '+CHAPTERS[i+1][1]+']('+CHAPTERS[i+1][0]+')')
    return ' · '.join(links)


INTRO = {
 1:('What is the study trying to establish?',
    'The pilot asks what evidence can justify a claim that an AI safeguard operated in a Catholic institutional setting. '
    'Read the present position first. The complete, dated scoping record is retained below; the later chapters contain the results and source records.'),
 2:('What was planned, and what is still open?',
    'This chapter contains the full governing protocol and its recorded amendment. The main comparative protocol remains 0.3.0 and unfrozen. '
    'Historical status statements in that document describe their original checkpoints, not the later live-response collection.'),
 3:('What did the first engineering comparison find?',
    'The complete checklist and structured gate made the same decisions on the 24 prepared packets. '
    'Neither procedure established whether a cited passage supports a theological claim. This chapter retains the complete results, freeze, source packet and execution boundaries.'),
 4:('Which institutional obligations might be relevant?',
    'Keep the source, its interpretation, institutional applicability, and observed control operation separate. '
    'The candidate mappings below remain unreviewed proposals. The code checks their records; it does not decide canon law or confer approval.'),
 5:('What did Magisterium AI actually answer?',
    'The six answers below are recorded service outputs, not verified advice. All questions were submitted once under the retained plan. '
    'Read each exact prompt, answer and returned reference list before drawing conclusions.'),
 6:('Which five risks are we investigating?',
    'These are the complete scenario drafts and source metadata. Draft-time status fields remain intact. '
    'Later execution status is reported in the study chapter and the separate run chapters; none of these drafts is a validated Catholic incident.'),
 7:('Where did AI contribute, and what did people review?',
    'This chapter brings together the study disclosure, contribution record and retained publication-guidance checks. '
    'Authorization to work, personal verification, qualified interpretation and publication approval remain separate. No new policy check or human attestation is implied by this reorganization.'),
 8:('What was decided, and how can a reviewer challenge it?',
    'The decision records and review worksheet are retained here in full. A later reader should be able to challenge a source, method, interpretation or conclusion separately. '
    'No worksheet entry is filled merely because an automated check passes.'),
 9:('Can someone inspect the evidence without relying on this conversation?',
    'The notebooks are the reading interface. Preserved source files, machine-readable evidence and code remain the research record. '
    'This chapter explains the record hierarchy, offline replay and earlier editions. No historical file is deleted or silently rewritten.'),
 10:('What makes the evidence inspectable?',
    'The full earlier evidence-workbench review follows. It is retained methodological material, with its original scope and date. '
    'The current study and run chapters report subsequent work; earlier statements about pending work are not silently changed.'),
 11:('What did the research course contribute?',
    'This is the full retained course-alignment review. It separates instructional design lessons from this pilot’s evidence and independent-review requirements. '
    'No LangChain runtime, multi-agent panel or new study is created by converting the material to notebook chapters.'),
}


def build(working_copy: bool = False) -> None:
    import nbformat
    src=Sources(working_copy)
    mds=src.markdowns()
    mapping={p:chapter_for(p) for p in mds}
    mapping.update({'study-report.html':1,'study-guide.ipynb':1,'protocol.html':2})
    chapters=[]
    for i,(name,title,desc) in enumerate(CHAPTERS):
        cells=[md('![Node & Norm: Catholic institutional AI research](assets/book-banner.svg)\n\n# '+f'{i:02d}. '+title+'\n\n'+navigation(i))]
        if i:
            question, explanation=INTRO[i]
            cells += [md('## '+question+'\n\n'+explanation+'\n\n'
             '**Reading status:** exploratory research; qualified review pending. '
             '**Book edition:** 1.0.0-navigation. **Evidence snapshot:** `'+BASE[:7]+'`.')]
        chapters.append(cells)
    toc='| Chapter | What you can inspect |\n| :--- | :--- |\n'+'\n'.join(
      '| ['+f'{i:02d}. '+title+']('+name+') | '+desc+' |' for i,(name,title,desc) in enumerate(CHAPTERS) if i)
    status='''## Where the pilot stands

| Completed and retained | What it establishes | What remains open |
| :--- | :--- | :--- |
| Five institutional scenario drafts | Specific questions and candidate safeguards | Independent scenario and source review |
| One 24-packet citation-identity comparison | Checklist and structured gate tied on these constructed cases | General validity, human benefit and semantic support |
| Six live Magisterium Q&A responses | What the service returned on six fixed requests | Verification of the returned authorities and qualified interpretation |
| Candidate obligations and authority records | Sources and questions to investigate | Canonical applicability and actual institutional approval |

**No institutional compliance conclusion, ecclesial endorsement or validated safeguard benefit is claimed.**
The main comparative protocol remains **0.3.0 and unfrozen**. The material is ready to inspect; the study is not complete.
'''
    chapters[0] += [md('## Read the study, not the folder structure\n\n'
      'This is the Catholic pilot’s primary reading home. Every chapter is a real Jupyter notebook with the relevant narrative, records and limits. '
      'You can read the saved pages without running code. Only the few record-check cells require a repository checkout.\n\n'
      '**Start with [the study and roadmap](01_Study_and_Roadmap.ipynb).** '
      'For a direct examination of the first result, open [citation-test results](03_Citation_Test_Results.ipynb).'),md(toc),
      md('## Choose your route\n\n'
      '| Reader | Suggested route |\n| :--- | :--- |\n'
      '| Catholic leaders and institutional reviewers | [Study](01_Study_and_Roadmap.ipynb) → [Results](03_Citation_Test_Results.ipynb) → [Live answers](05_Live_Parish_Responses.ipynb) → [Review](08_Decisions_and_Review.ipynb) |\n'
      '| Theologians and canonical advisers | [Context](04_Canon_Law_and_Authority.ipynb) → [Exact answers](05_Live_Parish_Responses.ipynb) → [Disclosure](07_AI_Disclosure.ipynb) → [Review worksheet](08_Decisions_and_Review.ipynb) |\n'
      '| Researchers and technical reviewers | [Protocol](02_Research_Protocol.ipynb) → [Test](03_Citation_Test_Results.ipynb) → [Scenarios](06_Risk_Scenarios_and_Sources.ipynb) → [Reproduction](09_Reproduce_and_Inspect.ipynb) |'),md(status),
      md('## The rule for interpreting evidence\n\n![Evidence sequence: source identity, meaning, applicability, observed operation, qualified review](assets/evidence-path.svg)\n\n'
      'A correct citation is not proof of a sound interpretation. A plausible interpretation is not proof that a control operated. '
      'A passing software check is not independent human review.'),
      md('## Reading, archives and disclosure\n\n'
      'The current reading path contains notebooks only. Original Markdown, HTML and PDF editions remain in the preserved historical record so prior citations and tests continue to work. '
      'You do not have to navigate them to read this book. [Archive and provenance](09_Reproduce_and_Inspect.ipynb) explains their role.\n\n'
      'This reorganization was prepared with AI assistance. It adds navigation and presentation, not new experiments, review judgments or source verification. '
      '[Read the disclosure](07_AI_Disclosure.ipynb).')]
    study=src.obj('study.json')
    chapters[1] += [md(status),md('## Research question\n\n'+pretty(study['primary_question'])),
      md('## Proposed contribution\n\n'+pretty(study['contribution'])+'\n\n### Competing explanation\n\n'+pretty(study['alternative'])),
      md('## Planned hypotheses\n\nThese remain hypotheses, not established findings.\n\n'+pretty(study['hypotheses'])),
      md('## Practical sequence from here\n\n'
      '| Step | Required evidence |\n| :--- | :--- |\n'
      '| Verify claims in the six answers | Located original passages, edition checks and retained discrepancies |\n'
      '| Obtain qualified review | Reviewer competence, prior AI exposure, judgments, disagreements and limitations |\n'
      '| Prepare the next controlled test | Fixed system, source condition, cases, comparator and measurement plan |\n'
      '| Update findings | New run records and explicit changes; preserve earlier outputs |\n\n'
      'This sequence restates the open gates in the retained source records; it does not announce new execution.'),
      md('## Original seven-stage roadmap\n\n**Historical planning snapshot from `study.json`.** Stage labels below are retained, not newly adjudicated completion decisions.\n\n'+pretty(study['stages']))]
    preferred={'RESULTS.md':0,'PROTOCOL.md':0,'README.md':1,'SCOPING.md':0,'FREEZE.md':2,'SOURCE_PACKET.md':3}
    coverage=[]
    for rel in sorted(mds,key=lambda p:(chapter_for(p),preferred.get(Path(p).name,5),p)):
        add_source(chapters[chapter_for(rel)],rel,src,mapping,coverage)
    for idx,rel,title,key in [
      (4,OA+'sources.json','Official source-page register','sources'),
      (4,OA+'mappings.json','Five candidate obligation mappings','mappings'),
      (4,'data/normative-crosswalk.json','Eighteen inherited teaching mappings','records'),
      (6,'scenario-batches/CB-001/candidates.json','Five complete scenario drafts','candidates'),
      (7,'disclosure/record.json','Study contribution and actual-review record',None),
      (7,'disclosure/historical-guidance-2026-10-27.json','Historical publication guidance',None),
      (7,'disclosure/policy-checks.json','Retained policy-access checks',None),
      (8,OA+'decision-record.json','Obligations-stage decisions and disclosure',None),
      (8,'evidence-workbench/decisions.json','Evidence-workbench decision register',None),
    ]:
        add_json(chapters[idx],rel,src,title,key)
    evidence=src.obj(PQA+'evidence.json')
    chapters[5].append(md('## Exact recorded questions and answers\n\n'
       'The text below reproduces each retained prompt, generated answer and reference object. '
       'References are returned metadata, not independently established authorities. Provider-internal retrieval, model settings and session independence remain unknown.'))
    for row in evidence['records']:
        r=row['response']
        chapters[5].append(md('## '+row['case_id']+'\n\n### Exact submitted prompt\n\n'+row['prompt']+
          '\n\n### Recorded Magisterium answer\n\n'+r['answer']+
          '\n\n### Returned references\n\n'+pretty(r['references'])+
          '\n\n### Capture fields\n\n'+pretty({k:v for k,v in row.items() if k not in {'prompt','response'}}),
          kind='record_projection',source_path=EXT+'/'+PQA+'evidence.json',source_commit=BASE,
          record=row['case_id'],response_sha256=digest(json.dumps(r,ensure_ascii=False,sort_keys=True).encode())))
    for path in ['reading/archive-support/cir001/replay-inputs/cases.json', 'reading/archive-support/cir001/replay-inputs/raw-results.replay.json']:
        src.read(path)
    chapters[3] += [md('## Recount the retained comparison\n\nRun the following cell only to recount the stored replay records. It does not issue new requests or establish an independent reference standard.'),
       code(OFFLINE_ROOT+'''cases = json.loads((E / 'reading/archive-support/cir001/replay-inputs/cases.json').read_text())
rows = json.loads((E / 'reading/archive-support/cir001/replay-inputs/raw-results.replay.json').read_text())
assert len(cases) == 24 and len(rows) == 72
assert all(r['output']['semantic_support'] == 'unreviewed' and r['output']['answer_verified'] is False for r in rows)
print('Retained comparison:', len(cases), 'prepared packets;', len(rows), 'deterministic outputs.')
print('This recount is not a new experiment or a theological judgment.')
''')]
    chapters[4] += [md('## Check the applicability records\n\nThis checks references and recorded pending states; it does not interpret the law.'),
       code(OFFLINE_ROOT+'''sources = json.loads((E / 'scenario-batches/CB-001/obligations/sources.json').read_text())
maps = json.loads((E / 'scenario-batches/CB-001/obligations/mappings.json').read_text())
ids = {r['id'] for r in sources['sources']}
for row in maps['mappings']:
    assert set(row['source_ids']) <= ids
    assert row['assessment']['canonical_applicability'] == 'pending_qualified_review'
    assert row['assessment']['compliance_conclusion'] == 'not_assessed'
    assert row['assessment']['approval_record'] is None
print(len(sources['sources']), 'source-page records;', len(maps['mappings']), 'candidate applicability records.')
print('Qualified review remains pending; no compliance or approval determination.')
''')]
    chapters[5] += [md('## Recount the captured responses\n\nThis validates the inventory of retained responses and reference entries, not the correctness of the answers.'),
       code(OFFLINE_ROOT+'''packet = json.loads((E / 'scenario-batches/CB-001/PARISH-QA-001-R1/evidence.json').read_text())
records = packet['records']
refs = [r for x in records for r in x['response']['references']]
urls = {r['source_url'] for r in refs}
assert len(records) == 6 and len(refs) == 40 and len(urls) == 38
print(len(records), 'recorded responses;', len(refs), 'reference entries;', len(urls), 'distinct URLs.')
print('No new service calls. No correctness, compliance or independence score.')
''')]
    chapters[8].insert(2,md('## This navigation decision\n\n'
       '**User request:** bring the Catholic pilot to the repository front and provide notebooks as the reading format.\n\n'
       '**Implemented approach:** import the complete retained prose into numbered notebook chapters; display the machine records alongside the relevant text; retain old files as provenance. '
       'Retarget reader links to notebooks, add a root entry notebook and one bounded README navigation link, and preserve the previous root README text outside that addition.\n\n'
       '**Alternatives rejected:** deleting cited historical sources; moving raw evidence and breaking existing checks; retaining a navigation page that only sends readers to Markdown.\n\n'
       '**Scientific effect:** none. No model run, canonical judgment, review attestation or hypothesis change. '
       'User authorization is a maintenance authorization, not independent scientific review.'))
    chapters[9].insert(2,md('## Record hierarchy and execution\n\n'
       '1. The fixed source snapshot preserves the original record.\n'
       '2. This notebook book provides the complete reading interface.\n'
       '3. Original datasets and run receipts support the displayed findings.\n'
       '4. Git commits and prior editions preserve changes.\n\n'
       'Clone the repository and read `CATHOLIC_PILOT.ipynb`. In a notebook environment, open the numbered chapters in `catholic-ai-pilot/`. '
       'The three short executable chapters read local records only. They are optional for reading.\n\n'
       'The book contains a notebook-only `myst.yml` table of contents for Jupyter Book tooling. This change does not deploy a website. '
       'GitHub renders the notebooks as static pages. A book-tool build, if performed separately, must not be described as new research.\n\n'
       '**Preservation:** archived Markdown/HTML/PDF files and saved notebook outputs remain unchanged. '
       'Source text in imported notebook cells is retained in provenance metadata. A coverage manifest records where every active source document was imported. '
       'The reorganization never converts missing historical records into completed evidence.'))
    chapters[9].append(md('## Archived notebook editions\n\n'+ '\n'.join(
        '- ['+v+' complete study notebook]('+REPO_URL+'/blob/'+BASE+'/'+EXT+'/reading/editions/'+v+'-draft/NodeNorm_Notebook_v'+v.replace('.','_')+'.ipynb)'
        for v in ['0.4.2','0.4.3','0.4.4'])))
    out=ROOT/BOOK;out.mkdir(parents=True,exist_ok=True)
    for i,(filename,title,_) in enumerate(CHAPTERS):
        chapters[i].append(md('---\n\n'+navigation(i)))
        nb=nbformat.from_dict(notebook(chapters[i],title));nbformat.validate(nb)
        nbformat.write(nb,out/filename)
    front=copy.deepcopy(chapters[0])
    for c in front:
        c['source']=c['source'].replace('(assets/','('+BOOK+'/assets/')
        c['source']=re.sub(r'\]\((\d\d_[^)]+\.ipynb)\)',lambda m:']('+BOOK+'/'+m.group(1)+')',c['source'])
    nbformat.write(nbformat.from_dict(notebook(front,'Catholic institutional AI pilot')),ROOT/ENTRY)
    assets=out/'assets';assets.mkdir(exist_ok=True)
    (assets/'book-banner.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 170" role="img" aria-label="Node and Norm Catholic AI pilot"><rect width="1040" height="170" rx="15" fill="#1c1923"/><text x="35" y="42" font-family="sans-serif" font-size="15" fill="#c6beff" letter-spacing="2">NODE &amp; NORM · NOTEBOOK BOOK</text><text x="35" y="95" font-family="sans-serif" font-size="36" font-weight="bold" fill="#ffffff">Catholic institutional AI pilot</text><text x="35" y="134" font-family="sans-serif" font-size="18" fill="#e5e2f1">Questions, sources, methods, results and review, in one guided collection.</text></svg>''')
    labels=['Source identity','Meaning','Applicability','Control operation','Qualified review']
    svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 125" role="img" aria-label="Separate questions require separate evidence">'
    for i,label in enumerate(labels):
        x=8+i*207
        svg+=f'<rect x="{x}" y="15" width="190" height="78" rx="10" fill="#eeebf8" stroke="#d8d1e8"/><text x="{x+15}" y="44" font-family="sans-serif" font-size="14" fill="#5544b5">{i+1:02}</text><text x="{x+15}" y="73" font-family="sans-serif" font-size="16" fill="#24232b">{label}</text>'
        if i<4: svg+=f'<text x="{x+193}" y="62" font-family="sans-serif" font-size="16" fill="#5544b5">→</text>'
    (assets/'evidence-path.svg').write_text(svg+'</svg>')
    toc_config={'version':1,'project':{'title':'Catholic Institutional AI Risk and Control Evidence Pilot',
        'description':'Notebook-only exploratory research book. Qualified review remains pending.',
        'github':REPO_URL,'toc':[{'file':n,'title':t} for n,t,_ in CHAPTERS]},'site':{'template':'book-theme'}}
    (out/'myst.yml').write_text(json.dumps(toc_config,indent=2)+'\n')
    meta=out/'_provenance';meta.mkdir(exist_ok=True)
    manifest={'book_version':VERSION,'source_commit':BASE,'source_mode':'working_copy_local_check' if working_copy else 'git_commit',
       'root_entry':ENTRY,'chapters':[{'path':BOOK+'/'+n,'title':t} for n,t,_ in CHAPTERS],
       'source_documents':coverage,'inputs':list(src.used.values()),
       'new_research_results':False,'qualified_review':'pending','protocol':'0.3.0; unfrozen',
       'original_archive_modified':False,'new_standalone_markdown_or_html_readers':0,
       'transformation':'Full source text retained in provenance; notebook link retargeting only. JSON values displayed without inferred judgments.',
       'root_readme_exception':'One exact navigation block only; original remainder must match the baseline blob.'}
    (meta/'book-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (meta/'maintenance-disclosure.json').write_text(json.dumps({'kind':'AI_assisted_presentation_migration',
      'assistant':'ChatGPT (OpenAI)','provider_snapshot':'not_preserved_in_repository_record',
      'activities':['repository-source inspection','navigation design','source-preserving notebook conversion','software tests'],
      'new_model_under_test_calls':0,'new_qualified_review':False,'human_authorization':'User requested front-page notebook organization; no personal verification inferred.',
      'old_evidence_unchanged':True,'hosting':'No hosted site deployment requested by this migration.'},indent=2)+'\n')
    print(json.dumps({'chapters':len(CHAPTERS),'source_documents_imported':len(coverage),'source_mode':manifest['source_mode'],'new_research_results':False},indent=2))


def strip_navigation(data: bytes) -> bytes:
    if data.count(NAV.encode()) > 1:
        raise ValueError('Duplicate root navigation block.')
    return data.replace(NAV.encode(), b'')


def add_navigation() -> None:
    path=ROOT/'README.md';data=path.read_text()
    if NAV not in data:
        token='\n\nWhat can surviving records establish'
        if token not in data:raise ValueError('Root README layout changed; review before insertion.')
        data=data.replace(token,'\n'+NAV+'\nWhat can surviving records establish',1)
        path.write_text(data)
    legacy=ROOT/EXT/'README.md'
    original=legacy.read_text()
    prefix='> **Notebook reading home:** [Open the Catholic pilot book](../../../CATHOLIC_PILOT.ipynb). The files below remain the historical source and evidence workspace.\n\n'
    if not original.startswith(prefix):legacy.write_text(prefix+original)
    old_test = ROOT/'tests/test_catholic_reader_archive.py'
    s = old_test.read_text()
    token = "data = (REPO/'README.md').read_bytes()"
    replacement = token + "\n        import runpy\n        data = runpy.run_path(str(REPO/'scripts/build_catholic_notebook_book.py'))['strip_navigation'](data)"
    if "['strip_navigation']" not in s:
        if token not in s:raise ValueError('Archive test changed; inspect before adaptation.')
        old_test.write_text(s.replace(token,replacement,1))
    release_test = ROOT/EXT/'scripts/test_release.py'
    s=release_test.read_text()
    token='data=path.read_bytes();actual='
    replacement="data=runpy.run_path(str(ROOT.parents[2]/'scripts/build_catholic_notebook_book.py'))['strip_navigation'](path.read_bytes());actual="
    if "['strip_navigation']" not in s:
        if token not in s:raise ValueError('Release test changed; inspect before adaptation.')
        release_test.write_text(s.replace(token,replacement,1))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--working-copy',action='store_true',help='Local preparation only; never represents an authoritative Git-source check.')
    p.add_argument('--navigation',action='store_true');args=p.parse_args()
    build(args.working_copy)
    if args.navigation:add_navigation()
