#!/usr/bin/env python3
"""Apply shared AI disclosure to current readers. Offline; no research calls.
Run after the existing builder. Archive/history and root README are untouched.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile
ROOT = Path(__file__).resolve().parent.parent
VERSION = '0.1.0'
SUFFIX = 'v0_4_1'
BEGIN = '<!-- NODE_NORM_AI_DISCLOSURE_BEGIN -->'
END = '<!-- NODE_NORM_AI_DISCLOSURE_END -->'
NB_MARK = 'node_norm_ai_disclosure'

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def validate_record(r):
    errors=[]
    if r.get('version') != VERSION: errors.append('unexpected_disclosure_version')
    if not r.get('statement') or not r.get('contributions'): errors.append('missing_statement_or_contributions')
    ids=[x.get('id') for x in r.get('tools',[])]
    if len(ids)!=len(set(ids)): errors.append('duplicate_tool_id')
    for t in r.get('tools',[]):
        if t.get('model_snapshot') is None and not t.get('unknown_reason'): errors.append('unknown_model_without_reason')
    for c in r.get('contributions',[]):
        if not c.get('artifact_scope') or not c.get('evidence_basis'): errors.append('contribution_without_scope_or_basis')
        if any(t not in ids for t in c.get('tools',[])): errors.append('unknown_tool_reference')
        if not c.get('human_review_status') or not c.get('independent_review_status'): errors.append('review_status_missing')
    p=r.get('publication',{})
    if p.get('ai_authors'): errors.append('ai_cannot_be_author')
    if p.get('target_venue') is None and p.get('venue_compliance')!='pending_venue_selection_and_recheck': errors.append('venue_compliance_without_venue')
    h=r.get('human_review',{})
    if h.get('authorization_is_source_verification') or h.get('authorization_is_release_approval_for_all_claims'): errors.append('authorization_overclaim')
    for group in ['specific_personal_review_attestations','independent_review_attestations','qualified_theological_review_attestations']:
        for a in h.get(group,[]):
            if not all(a.get(k) for k in ['reviewer','artifact_version','scope','review_date','limitations','ai_exposure']): errors.append('incomplete_human_attestation')
    for k in ['historical_prompt_reconstruction_permitted','public_secrets_permitted','public_sensitive_institutional_data_permitted','private_internal_reasoning_claimed']:
        if r.get('retention',{}).get(k) is not False: errors.append('unsafe_retention_claim:'+k)
    return sorted(set(errors))

def markdown(r, policies):
    lines=['## AI assistance, human responsibility and review',f'**Disclosure {r["version"]} | {r["date"]} | Exact-text author review pending**','This addendum documents contributions and review limits. It does not change the study hypotheses, source-run outcomes or research approval status.']
    lines += r['statement']
    lines += ['### Inspect the contributions']
    table=['| Task and affected artifacts | Status and review boundary |','|---|---|']
    for c in r['contributions']:
        artifacts=', '.join('`'+p+'`' for p in c['artifact_scope'])
        table.append(f'| **{c["id"]}: {c["task"]}**. {artifacts} | {c["evidence_basis"]}. Human review: `{c["human_review_status"]}`. Independent review: `{c["independent_review_status"]}`. |')
    lines.append('\n'.join(table))
    lines += ['### Actual human checks, not inferred approval','The contribution record contains no new personal, independent or qualified theological review attestation. A future attestation must name the person, exact artifact and claim scope, inspection method, prior AI exposure, conflicts, disposition, limitations and date. Publication authorization is recorded separately.','### Guidance and current access qualifications','The user-supplied October 27 register remains a historical record. The following November 6 checks are a separate comparison, not a universal standard or compliance certification.']
    for p in policies['checks']:
        title='['+p['source']+']('+p['url']+')' if p.get('url') else p['source']
        lines += [f'**{p["rule_id"]} · {title}.** {p["bounded_summary"]} Access: {p["access"]} Action: {p["study_action"]}']
    lines += ['### Scope of documentation','Current HTML, notebook, protocol and reading PDF share this disclosure. Earlier archived editions retain their original bytes and are qualified through this dated register. Material AI use in new code, analysis, figures, data preparation, or report revisions requires an artifact-scoped record. Routine edits may be grouped; substantive changes and research runs require individual records.','For an actual multi-agent run, retain parent and child run IDs, role, provider/model metadata as exposed, application prompt and input references, outputs, errors, retries, stopping reason and human decisions. A named AI persona is not a human specialist. Do not expose hidden model reasoning or claim a complete internal trace; record observable actions and concise decision rationales.','### Policy hierarchy','[Node & Norm research-integrity commitments]('+r['governing_program_policy']+') supply the program baseline. CEC\'s AI-use policy governs this repository. This record implements the study-specific account. [TAE\'s November disclosure]('+r['tae_reference']+') is a methodological precedent, not evidence that TAE\'s reviewers or experiments participated here. Venue rules are a separate submission-stage check.','Machine checks can confirm field presence and shared disclosure text. They cannot establish source truth, human independence, theological validity, or publisher acceptance.']
    return '\n\n'.join(lines)+'\n'

def strip_block(text):
    return re.sub(re.escape(BEGIN)+r'.*?'+re.escape(END),'',text,flags=re.S).rstrip()

CSS='''
.ai-use-notice{border:1px solid var(--line,#dedbe4);border-radius:10px;padding:12px 16px;margin:24px 0 4px;background:var(--lav,#f0edf8);font-size:14px;line-height:1.6}.ai-disclosure{overflow-wrap:anywhere}.ai-disclosure details{border:1px solid var(--line,#dedbe4);border-radius:12px;background:white;padding:18px 22px}.ai-disclosure summary{cursor:pointer;font-size:18px}.ai-disclosure-body{padding-top:16px;font-size:16px;line-height:1.7}.ai-disclosure-body h2{font-size:27px}.ai-disclosure-body h3{font-size:21px;margin-top:28px}.ai-table{overflow-x:auto}.ai-table table{width:100%;border-collapse:collapse;font-size:13px;line-height:1.6}.ai-table td,.ai-table th{border:1px solid var(--line,#dedbe4);padding:12px;vertical-align:top;text-align:left}.ai-table th{background:var(--lav,#f0edf8)}.ai-disclosure a,.ai-disclosure code{overflow-wrap:anywhere;word-break:break-word}@media(max-width:760px){.ai-disclosure details{padding:15px}.ai-table table{min-width:540px}.ai-disclosure-body{font-size:15px}}@media print{.ai-disclosure{break-inside:auto!important}.ai-disclosure details{border:0;padding:0}.ai-disclosure summary{font-size:12pt;break-after:avoid}.ai-disclosure-body{display:block!important;font-size:9pt;line-height:1.5}.ai-disclosure-body h2{font-size:17pt}.ai-disclosure-body h3{font-size:12pt;break-after:avoid}.ai-table{overflow:visible}.ai-table table{font-size:8pt;table-layout:fixed;min-width:0}.ai-table td,.ai-table th{padding:7px}.ai-table tr{break-inside:avoid}.ai-use-notice{font-size:9pt}}
'''

def patch_html(original,r,policies,text):
    import mistune
    render=mistune.create_markdown(escape=True,plugins=['table'])
    body=render(text).replace('<table>','<div class="ai-table"><table>').replace('</table>','</table></div>')
    section=BEGIN+'<section class="section ai-disclosure" id="ai-use-disclosure"><div class="eyebrow">Research integrity · AI assistance</div><details open><summary><strong>What AI contributed and what people have actually reviewed</strong></summary><div class="ai-disclosure-body">'+body+'</div></details></section>'+END
    original=strip_block(original)
    original=re.sub(r'<!-- AI_USE_NOTICE_BEGIN -->.*?<!-- AI_USE_NOTICE_END -->','',original,flags=re.S)
    original=re.sub(r'/\* AI_USE_STYLE_BEGIN \*/.*?/\* AI_USE_STYLE_END \*/','',original,flags=re.S)
    if '</main>' not in original or '</style>' not in original: raise ValueError('Expected main/style elements missing.')
    original=original.replace('</style>','/* AI_USE_STYLE_BEGIN */'+CSS+'/* AI_USE_STYLE_END */</style>',1)
    notice='<!-- AI_USE_NOTICE_BEGIN --><aside class="ai-use-notice">Substantive AI assistance is disclosed. Specific human verification remains bounded. <a href="#ai-use-disclosure">Read contributions and review status</a>. Disclosure addendum 0.1.0.</aside><!-- AI_USE_NOTICE_END -->'
    original=re.sub(r'(<main\b[^>]*>)',lambda m:m.group(1)+notice,original,count=1)
    return original.replace('</main>',section+'</main>',1)+'\n'

def patch_notebook(path,r,policies,text,execute=False):
    import nbformat
    nb=nbformat.read(path,as_version=4)
    nb.cells=[c for c in nb.cells if not c.metadata.get(NB_MARK)]
    md=nbformat.v4.new_markdown_cell(text,id='ai-use-disclosure');md.metadata[NB_MARK]=True
    source='# Offline disclosure-record checks. No model calls or human approval inferred.\nimport json\nAI_DISCLOSURE = json.loads('+repr(json.dumps(r,ensure_ascii=False))+')\nassert AI_DISCLOSURE["publication"]["ai_authors"] == []\nassert AI_DISCLOSURE["publication"]["target_venue"] is None\nassert AI_DISCLOSURE["human_review"]["authorization_is_source_verification"] is False\nassert all(x["independent_review_status"] == "pending" for x in AI_DISCLOSURE["contributions"])\nprint("Disclosure:", AI_DISCLOSURE["version"])\nprint("Six contribution records; exact model snapshots unknown where unrecorded.")\nprint("Independent and qualified review pending. No venue compliance certified.")\n'
    cell=nbformat.v4.new_code_cell(source,id='ai-use-checks');cell.metadata[NB_MARK]=True
    nb.cells[1:1]=[md,cell]
    nb.metadata['ai_disclosure']={'id':r['disclosure_id'],'version':r['version'],'canonical_record_sha256':hashlib.sha256((json.dumps(r,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),'human_review':'pending','venue_compliance':'pending'}
    if execute:
        from nbclient import NotebookClient
        NotebookClient(nb,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(path.parent)}}).execute()
    for c in nb.cells:c.metadata.pop('execution',None)
    nbformat.validate(nb);nbformat.write(nb,path)
    return sum(c.cell_type=='code' for c in nb.cells)

def pdf_from_html(source,dest):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        options={'headless':True}
        system=shutil.which('chromium')
        if system:options['executable_path']=system
        browser=p.chromium.launch(**options)
        page=browser.new_page(viewport={'width':1440,'height':1100})
        page.route('**/*',lambda route:route.abort())
        page.set_content(source.read_text(encoding='utf-8'),wait_until='load')
        page.evaluate('document.querySelectorAll("details").forEach(x=>x.open=true)')
        page.pdf(path=str(dest),format='Letter',print_background=True,margin={'top':'16mm','bottom':'16mm','left':'15mm','right':'15mm'})
        browser.close()

def apply(root,execute=False,pdf=False,package=False):
    r=load(root/'disclosure/record.json');p=load(root/'disclosure/policy-checks.json')
    errors=validate_record(r)
    if errors:raise ValueError('; '.join(errors))
    text=markdown(r,p)
    (root/'AI_DISCLOSURE.md').write_text('# Study-specific AI disclosure\n\n'+text,encoding='utf-8')
    prot=root/'PROTOCOL.md'
    if prot.exists():prot.write_text(strip_block(prot.read_text(encoding='utf-8'))+'\n\n'+BEGIN+'\n'+text+END+'\n',encoding='utf-8')
    for name in ['study-report.html','protocol.html']:
        path=root/name;path.write_text(patch_html(path.read_text(encoding='utf-8'),r,p,text),encoding='utf-8')
    nbc=patch_notebook(root/'study-guide.ipynb',r,p,text,execute)
    out=root/'reading';out.mkdir(exist_ok=True)
    names={'study-report.html':f'NodeNorm_Study_{SUFFIX}.html','protocol.html':f'NodeNorm_Protocol_{SUFFIX}.html','PROTOCOL.md':f'NodeNorm_Protocol_{SUFFIX}.md','study-guide.ipynb':f'NodeNorm_Notebook_{SUFFIX}.ipynb'}
    for src,dst in names.items():shutil.copyfile(root/src,out/dst)
    if pdf:pdf_from_html(out/names['study-report.html'],out/f'NodeNorm_Study_{SUFFIX}.pdf')
    files=list(names.values())
    if pdf:files.append(f'NodeNorm_Study_{SUFFIX}.pdf')
    manifest={'reader_update':'0.4.1-dev','underlying_study':'0.4.0-dev','protocol_methods':'0.3.0-unfrozen','disclosure_version':VERSION,'date':'2026-11-06','scope':'Disclosure-only update; no new empirical observations or methodology results.','files':[{'path':n,'sha256':hashlib.sha256((out/n).read_bytes()).hexdigest(),'bytes':(out/n).stat().st_size} for n in files]}
    save(out/'DISCLOSURE_READING_MANIFEST.json',manifest)
    coverage={'version':VERSION,'method':'Rendered from disclosure/record.json and policy-checks.json','primary_artifacts':['AI_DISCLOSURE.md','PROTOCOL.md','study-report.html','protocol.html','study-guide.ipynb'],'reading_files':files,'notebook_code_cells':nbc,'notebook_executed':execute,'pdf_rendered':pdf,'historical_archives_modified':False,'root_readme_modified':False,'independent_validation':False,'venue_compliance':'pending'}
    save(root/'disclosure/coverage.json',coverage)
    if package:
        with zipfile.ZipFile(out/f'NodeNorm_AI_Disclosure_Update_{SUFFIX}.zip','w',zipfile.ZIP_DEFLATED) as z:
            for n in files+['DISCLOSURE_READING_MANIFEST.json']:z.write(out/n,'readers/'+n)
            for path in sorted((root/'disclosure').rglob('*')):
                if path.is_file():z.write(path,'repository/'+str(path.relative_to(root)))
            for n in ['AI_DISCLOSURE.md','scripts/apply_ai_disclosure.py','scripts/test_ai_disclosure.py']:
                if (root/n).is_file():z.write(root/n,'repository/'+n)
            z.writestr('START_HERE.txt','Open readers/NodeNorm_Study_v0_4_1.html or the PDF. The notebook runs offline. This package documents AI assistance, not human approval. The disclosure-only update is additive to existing study sources. Historical guidance and fresh checks remain separate.\n')
    return coverage

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--execute',action='store_true');parser.add_argument('--pdf',action='store_true');parser.add_argument('--package',action='store_true')
    args=parser.parse_args();print(json.dumps(apply(args.root,args.execute,args.pdf,args.package),indent=2))
