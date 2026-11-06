#!/usr/bin/env python3
"""Build synchronized Catholic pilot reading files. Offline; no research API calls.

Inputs: release.json, archived design files, METHOD_AMENDMENT.md, SCOPING.md,
source JSON, and a captured development run. Legacy aesthetic retained.
"""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import html
import io
import json
import re
import runpy
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def derive(capture):
    records = capture['records']
    if len(records) != 4:
        raise ValueError('The bounded run must retain all four recorded calls.')
    plan_bytes = (json.dumps(capture['plan'], indent=2) + '\n').encode()
    if hashlib.sha256(plan_bytes).hexdigest() != capture['plan_sha256']:
        raise ValueError('Pre-call plan bytes do not match the retained hash.')
    rows = []
    for i, target in enumerate(capture['plan']['queries']):
        search, fetch = records[2*i:2*i+2]
        assert search['request']['query'] == target['query']
        chosen = next((r for r in search['response']['returned_items'] if r['id'] == fetch['request']['id']), None)
        if chosen is None:
            raise ValueError('Fetch identifier absent from the recorded search.')
        expected = chosen['url'].rstrip('/').split('/')[-1]
        actual = fetch['response'].get('metadata', {}).get('ref')
        outcome = 'fetch_not_found' if not fetch['response'].get('found') else ('locator_match' if actual == expected else 'locator_mismatch')
        rows.append({'target': target['target'], 'search_locator': expected, 'fetched_locator': actual, 'outcome': outcome})
    return rows

def md_cell(text):
    return {'cell_type':'markdown','metadata':{},'id':'m-'+hashlib.sha256(text.encode()).hexdigest()[:12],'source':text}

def code_cell(text):
    return {'cell_type':'code','metadata':{},'id':'c-'+hashlib.sha256(text.encode()).hexdigest()[:12],'source':text,'execution_count':None,'outputs':[]}

def build():
    import mistune
    render = mistune.create_markdown(escape=True, plugins=['table'])
    release = read_json(ROOT/'release.json')
    capture = read_json(ROOT/'runs'/release['run']/'capture.json')
    rows = derive(capture)
    run_dir = ROOT/'runs'/release['run']
    save_json(run_dir/'plan.json',capture['plan'])
    for record in capture['records']:save_json(run_dir/(record['record_id']+'.json'),record)
    save_json(run_dir/'05-original-checks.json',capture['official_checks'])
    save_json(run_dir/'results.json',capture['reported_results'])
    study = read_json(ROOT/'archive/v0.2/study.json')
    study.update(version=release['version'], status=release['status'], snapshot_label='Pilot initiation snapshot · 6 November 2026')
    study['warning']='One bounded source-verification run is recorded. Its two selected search/fetch pairs did not yield their requested verified passages. Eighteen normative mappings remain unreviewed; zero Catholic empirical cases are admitted and no Catholic safeguard evaluation is completed.'
    study['current']=[{'value':release['protocol_version'],'label':'Protocol edition','note':'Main comparative protocol remains unfrozen'}, {'value':'1','label':'Source-verification run','note':'Two targets; four MCP calls; no retries'}, {'value':'0','label':'Catholic safeguard studies completed','note':'Independent research gates remain open'}, {'value':'18','label':'Source mapping candidates','note':'Qualified Catholic review pending'}]
    study['changes'].insert(0, {'date':release['date'],'version':release['version'],'description':'Consolidated the scoping chapter, evidence workbench, course alignment and first prospectively planned source-verification run into the five reading files. Preserved failed retrievals and separate research gates.'})
    study['stages'][0]['actions'][0]='Protocol 0.3.0 includes a bounded source-verification amendment; the main comparison remains unfrozen.'
    study['stages'][0]['actions'].append('SV-20261106-001 completed with two unresolved target retrievals; source capture and limitations are retained.')
    study['stages'][1]['dependency']='Requires a deliberately versioned upstream snapshot; no new ingestion is triggered by this release.'
    study['source_integration']['verification_status']='Eighteen provisional mappings; legacy six-row locator summary retained separately from the new four-call run SV-20261106-001.'
    study['release'] = release
    study['pilot_run'] = {'id':release['run'],'kind':'source_verification','pairs':rows,'mcp_calls':4,'independent_review':False}
    save_json(ROOT/'study.json',study)
    protocol=(ROOT/'archive/v0.2/PROTOCOL.md').read_text(encoding='utf-8')
    protocol=protocol.replace('Research protocol 0.2.0 | Working design','Research protocol 0.3.0 | Main comparative design unfrozen')
    protocol=re.sub(r'\*\*Current state:\*\*[^\n]*','**Current state:** Source-verification pilot initiated with one bounded run. No Catholic safeguard test, independent normative review, or canonical empirical admission has been completed. The 18 mappings remain provisional. See Section 15 for the new run and capture limits.',protocol,count=1)
    protocol=protocol.replace('six-interaction locator check','six-row selected locator comparison').replace('six Magisterium source-locator tool interactions','six selected legacy Magisterium locator comparisons')
    protocol += '\n\n' + (ROOT/'METHOD_AMENDMENT.md').read_text(encoding='utf-8')
    (ROOT/'PROTOCOL.md').write_text(protocol,encoding='utf-8')
    with contextlib.redirect_stdout(io.StringIO()):
        layout=runpy.run_path(str(ROOT/'scripts/_legacy_layout.py'))
    css=layout['CSS']
    scoping=(ROOT/'SCOPING.md').read_text(encoding='utf-8')
    rows_md='| Target | Search locator | Fetch locator | Outcome |\n|---|---|---|---|\n'+''.join(f"| {x['target']} | {x['search_locator']} | {x['fetched_locator'] or 'No passage'} | {x['outcome']} |\n" for x in rows)
    run_text='''## Pilot 01. A source must resolve before it can support a finding

**SV-20261106-001 · Exploratory source verification · Four MCP calls · No retries**

The plan was written before these calls. The targets were selected with knowledge of earlier locator anomalies; this is a purposive recheck, not a blind reliability estimate.

'''+rows_md+'''
The first returned identifier did not resolve. The second returned a different numbered paragraph. Both are retained without silent repair. The official Vatican check located the requested paragraphs and confirmed that the fetched Magnifica Humanitas opening belongs to paragraph 90, not 105.

**What follows:** neither selected pair provided its requested verified passage in this run. **What does not follow:** a general provider error rate, a provider-defect attribution, a theological conclusion, or a result about institutional safeguards.

The public record includes issued queries, all displayed search-result metadata, fetch metadata, the plan hash, local capture times and source-check notes. Full returned paragraph text is withheld pending rights review; its hash, length, short excerpt and omission reason remain visible. Local recorded-at times are not provider execution timestamps. The operator working copy has no established long-term archive custodian.

### Where to inspect the records

Read `runs/SV-20261106-001/capture.json`, `SCOPING.md`, the updated protocol, and the existing evidence workbench. The self-contained notebook recomputes the pair classifications offline. This reader calls no research services.

### Next work

Clarify identifier and chunk semantics or conduct a separately planned replication. Obtain qualified review of a few mappings, then prepare the first five institutional scenarios from a versioned upstream snapshot. No main-study gate has been waived.
'''
    extra_css='''
.pilot-reading{background:#fff;border:1px solid var(--line);border-radius:14px;padding:26px;margin:22px 0}.pilot-reading h2{font-size:29px}.pilot-reading h3{font-size:20px}.pilot-reading p{max-width:960px}.pilot-reading table,.protocol-reading table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.55;margin:20px 0}.pilot-reading th,.pilot-reading td,.protocol-reading th,.protocol-reading td{padding:12px;border:1px solid var(--line);text-align:left;vertical-align:top;overflow-wrap:anywhere}.pilot-reading th,.protocol-reading th{background:var(--lav)}.table-scroll{overflow-x:auto}code{overflow-wrap:anywhere}.protocol-reading{max-width:960px}.protocol-reading h1{font-size:35px}.protocol-reading h2{font-size:27px;margin-top:38px}.protocol-reading h3{font-size:21px}.protocol-reading{overflow-wrap:anywhere}@media print{h1,h2,h3,h4{break-inside:avoid!important;page-break-inside:avoid!important;orphans:3;widows:3}.section{break-inside:auto}.pilot-reading{break-inside:auto;padding:14px}.pilot-reading table,.protocol-reading table{font-size:8.5pt;table-layout:fixed}.pilot-reading th,.pilot-reading td,.protocol-reading th,.protocol-reading td{padding:6px}tr{break-inside:avoid}h2,h3,h4{break-after:avoid}.norm-groups,.two-cols,.hypotheses{display:block}.norm-group,.hypothesis{margin-bottom:12px;break-inside:auto}.norm-item{break-inside:avoid}.table-scroll{overflow:visible}.hero{grid-template-columns:1.5fr 1fr}.metric-grid{grid-template-columns:repeat(2,1fr)}.metric{min-height:0;padding:15px}.target-grid{grid-template-columns:repeat(3,1fr)}.end-panel{break-inside:avoid}.norm-head{break-after:avoid}.norm-item-body{padding:1px 14px 10px}.stage summary{display:block!important;break-after:avoid;break-inside:avoid;padding:12px 0}.stage-title{display:block!important}.stage-title strong{display:block;font-size:16px}.stage-title small{display:block;font-size:12px}.stage summary:after{display:none}.state{display:inline-block;margin:5px 0}.stage-n{display:block;margin-bottom:5px}.stage-body{padding:0 0 16px 20px;display:block}.hypothesis{break-inside:avoid;padding:18px}.hypo-top{break-after:avoid}.flow-grid,.objects-grid,.compare,.boundary-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}.flow-grid .process-step{padding:16px}.section h2{font-size:25px}.section-head{break-after:avoid}.pilot-reading h2{font-size:25px}}
'''
    render_safe=lambda s: render(s).replace('<table>','<div class="table-scroll"><table>').replace('</table>','</table></div>')
    addition='<section class="section" id="pilot-start"><div class="eyebrow">Current pilot evidence</div><div class="pilot-reading">'+render_safe(run_text)+'</div><details class="pilot-reading"><summary><strong>Chapter 1: the question, boundaries and capture plan</strong></summary>'+render_safe(scoping)+'</details></section>'
    study_html=(ROOT/'study-report.html').read_text(encoding='utf-8')
    study_html=study_html.replace('</style>',extra_css+'</style>',1).replace('<section class="section" id="readers">',addition+'<section class="section" id="readers">',1)
    study_html=study_html.replace('We have a research design, not findings.','The first source run is recorded.').replace('Source retrieval integrity: a small verification check','Legacy locator summary: six selected comparisons')
    study_html=study_html.replace('No results claimed','Source-verification outcomes only; no safeguard findings').replace('six-interaction check','six-row legacy comparison').replace('six-interaction','six-row legacy').replace('Planning release','Development release').replace('six interactions','six selected legacy rows')
    study_html=study_html.replace('on the dedicated CEC research branch','in the versioned Catholic study extension')
    study_html=study_html.replace('<div class="navlinks">','<div class="navlinks"><a href="#pilot-start">Pilot evidence</a>',1)
    study_html=study_html.replace('</body>','<script>window.addEventListener("beforeprint",()=>document.querySelectorAll("details").forEach(x=>x.open=true));</script></body>')
    (ROOT/'study-report.html').write_text(study_html,encoding='utf-8')
    protocol_html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Node &amp; Norm | Protocol 0.3.0</title><style>'+css+extra_css+'</style></head><body><header class="topbar"><nav class="nav"><span class="brand">node&amp;norm</span><span>Protocol 0.3.0 · Reading package 0.4.0-dev</span></nav></header><main class="protocol-reading">'+render_safe(protocol)+'</main></body></html>'
    (ROOT/'protocol.html').write_text(protocol_html,encoding='utf-8')
    nb=read_json(ROOT/'study-guide.ipynb')
    snapshot={'release':release,'study':study,'crosswalk':read_json(ROOT/'data/normative-crosswalk.json'),'legacy_audit':read_json(ROOT/'data/magisterium-locator-audit.json'),'capture':capture,'protocol_sha256':hashlib.sha256(protocol.encode()).hexdigest()}
    svg=(ROOT/'assets/workflow.svg').read_text(encoding='utf-8')
    snapshot_code='import json, hashlib\nSNAPSHOT = json.loads('+repr(json.dumps(snapshot,ensure_ascii=False))+')\nprint("Reading package:", SNAPSHOT["release"]["version"])\nprint("Protocol:", SNAPSHOT["release"]["protocol_version"])\nprint("Offline snapshot; no live repository or service query.")\n'
    revised=[nb['cells'][0],md_cell('## How to use this edition\n\nThis notebook contains the current study and captured source pilot. Run all cells offline, without companion files or API keys. Inputs are embedded and versioned. New service queries require a separate planned run. Source checks are not institutional safeguard findings.'),code_cell(snapshot_code),md_cell(scoping),md_cell(run_text)]
    for c in nb['cells'][1:]:
        src=''.join(c['source']) if isinstance(c['source'],list) else c['source']
        if c['cell_type']=='code':
            if 'SVG' in src:
                revised.append(code_cell('from IPython.display import display, SVG\ndisplay(SVG('+repr(svg)+'))\n'))
            elif 'crosswalk' in src:
                revised.append(code_cell('crosswalk = SNAPSHOT["crosswalk"]\nlegacy = SNAPSHOT["legacy_audit"]\nassert len(crosswalk["records"]) == 18\nassert len(legacy["tests"]) == 6\nprint("18 provisional mappings; six legacy comparison rows. Independent review pending.")\n'))
            else:
                revised.append(code_cell('assert len(SNAPSHOT["study"]["hypotheses"]) == 4\nassert len(SNAPSHOT["study"]["stages"]) == 7\nprint("Protocol SHA-256:", SNAPSHOT["protocol_sha256"])\nprint("Main research gates remain open; no institutional safeguard validation.")\n'))
        else:
            src=src.replace('six-interaction check','six-row legacy comparison').replace('Working research design · Not an empirical report','Source-verification development report · No safeguard findings')
            revised.append(md_cell(src))
    recompute='''# Recompute both classifications from the captured fields.
records = SNAPSHOT['capture']['records']
observed = []
for i, target in enumerate(SNAPSHOT['capture']['plan']['queries']):
    search, fetched = records[2*i:2*i+2]
    assert search['request']['query'] == target['query']
    choice = next(x for x in search['response']['returned_items'] if x['id'] == fetched['request']['id'])
    expected = choice['url'].rstrip('/').split('/')[-1]
    actual = fetched['response'].get('metadata', {}).get('ref')
    status = 'fetch_not_found' if not fetched['response'].get('found') else ('locator_match' if expected == actual else 'locator_mismatch')
    observed.append(status)
    print(target['target'], expected, '->', actual, ':', status)
assert observed == ['fetch_not_found', 'locator_mismatch']
plan_bytes = (json.dumps(SNAPSHOT['capture']['plan'], indent=2) + '\\n').encode()
assert hashlib.sha256(plan_bytes).hexdigest() == SNAPSHOT['capture']['plan_sha256']
print('Four recorded MCP calls; two purposive pairs; no retries. No general reliability estimate.')
'''
    revised.extend([md_cell('## Recompute the captured source run\n\nThese are actual recorded metadata, not synthetic controls. The classifier only compares fields; it cannot verify doctrinal meaning or independent reviewer eligibility.'),code_cell(recompute)])
    nb['cells']=revised
    nb['metadata']['node_and_norm'].update(manifest_version=release['version'],protocol_version=release['protocol_version'],network_required=False,source_run=release['run'],empirical_results=False)
    save_json(ROOT/'study-guide.ipynb',nb)
    out=ROOT/'reading';out.mkdir(exist_ok=True)
    copies={'study-report.html':'NodeNorm_Study_v0_4_0.html','study-guide.ipynb':'NodeNorm_Notebook_v0_4_0.ipynb','protocol.html':'NodeNorm_Protocol_v0_3_0.html','PROTOCOL.md':'NodeNorm_Protocol_v0_3_0.md'}
    for source,destination in copies.items():shutil.copyfile(ROOT/source,out/destination)
    legacy_path=ROOT/'evidence-workbench/repository-review.ipynb'
    if legacy_path.exists():
        legacy=read_json(legacy_path)
        for cell in legacy['cells']:
            text=''.join(cell['source']) if isinstance(cell['source'],list) else cell['source']
            cell['source']=text.replace("checks['verify_hashes'](ROOT.parent, inventory)","checks['verify_hashes'](ROOT.parent / 'archive/v0.2', inventory)")
        save_json(legacy_path,legacy)
    decisions=(ROOT/'archive/v0.2/DECISIONS.md').read_text(encoding='utf-8')
    decisions+='\n\n## 0.4.0-dev integration decision | 6 November 2026\n\nThe maintainer authorized repository integration, development release and branch cleanup. This operational authorization does not constitute independent methodological or ecclesial review. Preserve the main README and canonical study. Consolidate the current reading files through one builder, archive the v0.2 inputs, and record SV-20261106-001 without retry or silent repair. Source findings are separate from future safeguard findings. No other active branch or website ingestion is changed. The first run was performed by one assistant with tools; no multi-agent or independent human research panel is claimed.\n'
    (ROOT/'DECISIONS.md').write_text(decisions,encoding='utf-8')
    return release,rows

def execute_notebook():
    import nbformat
    from nbclient import NotebookClient
    import tempfile
    path=ROOT/'study-guide.ipynb'
    nb=nbformat.read(path,as_version=4)
    with tempfile.TemporaryDirectory() as work:
        NotebookClient(nb,timeout=120,kernel_name='python3',resources={'metadata':{'path':work}}).execute()
    for c in nb.cells:c.metadata.pop('execution',None)
    nb.metadata['language_info']={'name':'python','version':'3.11+'}
    nbformat.validate(nb);nbformat.write(nb,path)
    shutil.copyfile(path,ROOT/'reading/NodeNorm_Notebook_v0_4_0.ipynb')
    return sum(c.cell_type=='code' for c in nb.cells)

def pdf_and_visual_checks():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        executable=shutil.which('chromium') or shutil.which('google-chrome')
        browser=pw.chromium.launch(executable_path=executable,headless=True,args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1440,'height':1000})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.route('**/*',lambda route:route.abort())
        page.set_content((ROOT/'study-report.html').read_text(),wait_until='domcontentloaded')
        page.evaluate('document.fonts.ready')
        desktop=page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.click('#expand-all');assert page.locator('details.stage:not([open])').count()==0
        page.click('#collapse-all');assert page.locator('details.stage[open]').count()==0
        page.set_viewport_size({'width':390,'height':844})
        mobile=page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.set_viewport_size({'width':1440,'height':1000})
        page.evaluate('document.querySelectorAll("details").forEach(x=>x.open=true)')
        page.pdf(path=str(ROOT/'reading/NodeNorm_Study_v0_4_0.pdf'),format='Letter',print_background=True,margin={'top':'16mm','bottom':'17mm','left':'13mm','right':'13mm'},display_header_footer=True,header_template='<span></span>',footer_template='<div style="font-size:9px;color:#666;width:100%;text-align:center">Node &amp; Norm · Development 0.4.0 · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
        checks=ROOT/'validation';checks.mkdir(exist_ok=True)
        page.screenshot(path=str(checks/'study-desktop.png'),full_page=False)
        browser.close()
    if not desktop or not mobile or errors:raise AssertionError({'desktop':desktop,'mobile':mobile,'errors':errors})
    return {'desktop_width':1440,'mobile_width':390,'no_horizontal_overflow':desktop and mobile,'javascript_errors':errors,'roadmap_controls':'passed','all_pdf_sections_expanded':True}

def package():
    paths=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.zip','.png'} and p.name not in {'SHA256_MANIFEST.json','REPOSITORY_RECEIPT.json'})
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    save_json(ROOT/'reading/SHA256_MANIFEST.json',{'release':'0.4.0-dev','files':hashes,'meaning':'Byte integrity only; not source truth or independent review.'})
    dest=ROOT/'reading/NodeNorm_Catholic_Pilot_v0_4_0.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for p in paths:z.write(p,'NodeNorm_Catholic_Pilot_v0_4_0/'+str(p.relative_to(ROOT)))
        z.write(ROOT/'reading/SHA256_MANIFEST.json','NodeNorm_Catholic_Pilot_v0_4_0/reading/SHA256_MANIFEST.json')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true');parser.add_argument('--pdf',action='store_true');parser.add_argument('--package',action='store_true');args=parser.parse_args()
    rel,rows=build()
    report={'kind':'maintenance_checks','reading_version':rel['version'],'protocol_version':rel['protocol_version'],'source_pairs':rows,'scientific_validation':False}
    if args.execute:report['offline_code_cells_executed']=execute_notebook()
    if args.pdf:report['render_checks']=pdf_and_visual_checks()
    save_json(ROOT/'validation/release-checks.json',report)
    if args.package:package()
    print(json.dumps(report,indent=2))
