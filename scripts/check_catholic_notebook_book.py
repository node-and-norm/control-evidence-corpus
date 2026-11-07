#!/usr/bin/env python3
"""Validate the notebook book's custody and navigation; no scientific certification."""
from __future__ import annotations
import argparse, collections, hashlib, json, re, runpy, subprocess, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'catholic-ai-pilot'
BASE='c1628ae86186e2202ef82e1394f0b8bb8f7568ab'


def source_bytes(path, local=False):
    return (ROOT/path).read_bytes() if local else subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)


def check(local=False, execute=False):
    import nbformat
    manifest=json.loads((BOOK/'_provenance/book-manifest.json').read_text())
    builder=runpy.run_path(str(ROOT/'scripts/build_catholic_notebook_book.py'))
    files=[ROOT/'CATHOLIC_PILOT.ipynb']+[ROOT/r['path'] for r in manifest['chapters']]
    assert len(manifest['chapters'])==12
    assert manifest['new_research_results'] is False
    assert manifest['qualified_review']=='pending'
    assert not list(BOOK.rglob('*.md')) and not list(BOOK.rglob('*.html'))
    assert {p.name for p in BOOK.glob('*.ipynb')}=={Path(r['path']).name for r in manifest['chapters']}
    coverage={r['source']:r for r in manifest['source_documents']}
    projection=collections.defaultdict(list)
    pages=[]; executions=[]; links=0
    for file in files:
        nb=nbformat.read(file,as_version=4);nbformat.validate(nb)
        assert nb.metadata.node_norm.source_commit==BASE
        assert nb.metadata.node_norm.new_research_results is False
        if file.name!='CATHOLIC_PILOT.ipynb':
            for c in nb.cells:
                m=c.metadata.get('node_norm',{})
                if m.get('kind')=='source_text':
                    projection[m['source_path']].append((m['section'],m['original_text']))
                    assert m['source_path'] in coverage
        for c in nb.cells:
            if c.cell_type=='markdown':
                for dest in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',c.source):
                    if '://' in dest or dest.startswith(('#','mailto:','attachment:')):continue
                    path=dest.split('#')[0].split('?')[0]
                    if not path:continue
                    resolved=(file.parent/path).resolve()
                    assert resolved.is_relative_to(ROOT),str(resolved)
                    assert resolved.exists(),f'Broken link in {file.name}: {dest}'
                    assert not resolved.suffix in {'.md','.html','.pdf'},f'Reader sent to non-notebook: {dest}'
                    links+=1
        if execute and any(c.cell_type=='code' for c in nb.cells):
            from nbclient import NotebookClient
            NotebookClient(nb,timeout=90,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
            for c in nb.cells:
                c.metadata.pop('execution',None)
            nbformat.write(nb,file)
            executions.append({'notebook':str(file.relative_to(ROOT)),'code_cells':sum(c.cell_type=='code' for c in nb.cells),'kind':'offline_inventory_check','new_model_calls':0})
        pages.append({'path':str(file.relative_to(ROOT)),'cells':len(nb.cells),'code_cells':sum(c.cell_type=='code' for c in nb.cells)})
    assert set(projection)==set(coverage)
    for path, chunks in projection.items():
        restored=''.join(text for _,text in sorted(chunks))
        data=source_bytes(path,local)
        assert restored.encode()==data,'Incomplete source import: '+path
        assert hashlib.sha256(data).hexdigest()==coverage[path]['sha256']
    for item in manifest['inputs']:
        data=source_bytes(item['path'],local)
        assert hashlib.sha256(data).hexdigest()==item['sha256']
    packet=json.loads(source_bytes('research/extensions/catholic-institutions/scenario-batches/CB-001/PARISH-QA-001-R1/evidence.json',local))
    visible='\n'.join(c.source for c in nbformat.read(BOOK/'05_Live_Parish_Responses.ipynb',as_version=4).cells if c.cell_type=='markdown')
    for rec in packet['records']:
        assert rec['prompt'] in visible and rec['response']['answer'] in visible
        for ref in rec['response']['references']:
            assert ref['source_url'] in visible
    toc=json.loads((BOOK/'myst.yml').read_text())
    assert [x['file'] for x in toc['project']['toc']]==[Path(r['path']).name for r in manifest['chapters']]
    if not local:
        current=(ROOT/'README.md').read_bytes()
        old=source_bytes('README.md')
        assert builder['NAV'].encode() in current
        assert builder['strip_navigation'](current)==old
    report={'kind':'presentation_and_source_integrity_checks','source_commit':BASE,
       'source_mode':'working_copy_local_check' if local else 'git_commit','notebooks':pages,
       'complete_source_documents':len(coverage),'local_reader_links_checked':links,
       'source_reassembly_identical':True,'all_six_responses_preserved':True,
       'notebook_only_reader_path':True,'executions':executions,
       'new_research_results':False,'independent_validation':False,
       'note':'Source fidelity and code execution do not establish correctness of inherited claims or qualified review.'}
    if execute:
        report['output_hashes']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        (BOOK/'_provenance/validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in {'notebooks','output_hashes'}},indent=2))
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--working-copy',action='store_true');p.add_argument('--execute',action='store_true');a=p.parse_args()
    check(a.working_copy,a.execute)
