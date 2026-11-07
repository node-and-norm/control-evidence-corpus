#!/usr/bin/env python3
"""Archive delivered readers reproducibly; never run a research service.

Restored notebook metadata/outputs come from the delivered files. They are not
newly fabricated or new model runs. Every text/notebook export must match its
recorded original SHA-256. PDF reading copies are separately labelled renders.
"""
from __future__ import annotations
import argparse, base64, copy, hashlib, json, shutil, subprocess, sys, tempfile, zlib
from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parents[2]
BASELINE = '1ccac15b756558d58de6833910b7461c7f05e6d0'
PREFIX = 'research/extensions/catholic-institutions/'
SUPPORT = ROOT/'reading/archive-support'
META_SHA = 'ce13fafd57e54f0e8fdbf9d1210aaa34e327c2d259f997efba1960b3ca929548'
VERSIONS = ('0.4.2', '0.4.3', '0.4.4')

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def write_once(path: Path, data: bytes) -> None:
    if path.exists() and path.read_bytes() != data:
        raise ValueError(f'Refusing to overwrite a different archive: {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)

def git_bytes(relative: str) -> bytes:
    return subprocess.check_output(['git', 'show', f'{BASELINE}:{PREFIX}{relative}'], cwd=REPO)

def run(*args: str) -> None:
    subprocess.run([sys.executable, *map(str,args)], check=True)

def metadata() -> dict:
    data = zlib.decompress(base64.b64decode((SUPPORT/'retained-notebook-metadata.zlib.b64').read_text()))
    if digest(data) != META_SHA:
        raise ValueError('Retained notebook metadata checksum mismatch')
    write_once(SUPPORT/'retained-notebook-metadata.json', data)
    return json.loads(data)

def restore_notebook(directory: Path, version: str, entry: dict) -> None:
    name = f'NodeNorm_Notebook_v{version.replace(".","_")}.ipynb'
    path = directory/name
    notebook = nbformat.read(path, as_version=4)
    patch = entry['notebook']
    if 'metadata' in patch:
        notebook.metadata = patch['metadata']
    for item in patch['cells']:
        cell = notebook.cells[item['cell']]
        if digest(cell.source.encode()) != item['source_sha256']:
            raise ValueError(f'Changed notebook source: {version}, cell {item["cell"]}')
        cell.update(item['set'])
    nbformat.validate(notebook)
    nbformat.write(notebook, path)
    for filename, expected in entry['files'].items():
        data = (directory/filename).read_bytes()
        if digest(data) != expected['sha256'] or len(data) != expected['bytes']:
            raise ValueError(f'Delivered artifact mismatch: {version}/{filename}')

def execute_copy(path: Path) -> dict:
    from nbclient import NotebookClient
    nb = nbformat.read(path, as_version=4)
    before = digest(path.read_bytes())
    with tempfile.TemporaryDirectory() as empty:
        NotebookClient(copy.deepcopy(nb), timeout=120, kernel_name='python3',
                       resources={'metadata': {'path': empty}}).execute()
    if digest(path.read_bytes()) != before:
        raise ValueError('Replay changed the archived notebook')
    return {'code_cells': sum(c.cell_type == 'code' for c in nb.cells),
            'offline_replay_completed': True, 'archive_unchanged': True,
            'new_model_or_service_calls': 0, 'independent_validation': False}

def render_pdf(source: Path, target: Path) -> dict:
    from playwright.sync_api import sync_playwright
    if not target.exists():
        with sync_playwright() as pw:
            opts = {'headless': True}
            chromium = shutil.which('chromium') or shutil.which('chromium-browser')
            if chromium: opts['executable_path'] = chromium
            browser = pw.chromium.launch(**opts)
            page = browser.new_page(viewport={'width':1440, 'height':1000})
            # No remote source retrieval is necessary to render these self-contained files.
            page.route('**/*', lambda route: route.abort())
            page.set_content(source.read_text(), wait_until='load')
            page.evaluate('document.querySelectorAll("details").forEach(x=>x.open=true)')
            page.emulate_media(media='print')
            page.pdf(path=str(target), format='Letter', print_background=True,
                     margin={'top':'16mm','bottom':'16mm','left':'13mm','right':'13mm'})
            browser.close()
    return {'path':str(target.relative_to(ROOT)), 'sha256':digest(target.read_bytes()),
            'bytes':target.stat().st_size, 'origin':'repository_render_from_archived_html',
            'source_html_sha256':digest(source.read_bytes()),
            'original_attachment_pdf_byte_identity_claimed':False}

def build(execute: bool, pdf: bool) -> None:
    retained = metadata()
    baseline_readme = subprocess.check_output(['git','show',f'{BASELINE}:README.md'],cwd=REPO)
    if (REPO/'README.md').read_bytes()!=baseline_readme:
        raise ValueError('Root README protection check failed')
    index={'kind':'reader_artifact_archive','latest_draft':'0.4.4-draft',
           'published_release_preserved':'catholic-pilot-v0.4.1-dev',
           'baseline_commit':BASELINE,'core_protocol':'0.3.0; unfrozen',
           'new_research_results':False,'qualified_review':'pending','editions':{}}
    with tempfile.TemporaryDirectory() as folder:
        temp=Path(folder); baseline=temp/'baseline'; baseline.mkdir()
        for filename in ('study-report.html','study-guide.ipynb','protocol.html','PROTOCOL.md'):
            (baseline/filename).write_bytes(git_bytes(filename))
        cir=temp/'evidence'; cir.mkdir()
        # Use the repository's frozen recipe and digest-checked replay. This does
        # not create new observations or silently relabel a replay as a first run.
        cir_source=ROOT/'scenario-batches/CB-001/CIR-001'
        replay=temp/'replay'
        run(cir_source/'reproduce.py','--output',replay)
        for filename in ('cases.json','registry.json'):
            shutil.copy2(replay/filename,cir/filename)
        shutil.copy2(replay/'raw-results.replay.json',cir/'raw-results.json')
        for filename in ('engine.py','plan.json','execution.json'):
            (cir/filename).write_bytes(git_bytes('scenario-batches/CB-001/CIR-001/'+filename))
        for filename in ('build_readers.py','results.json','source-packet.json'):
            shutil.copy2(SUPPORT/'cir001'/filename,cir/filename)
        receipt=json.loads((cir/'execution.json').read_text())
        metrics=json.loads((cir/'results.json').read_text())
        original_metrics=(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n').encode()
        if digest(original_metrics)!=receipt['result_sha256']:
            raise ValueError('Original metric record changed')
        run(cir/'build_readers.py')
        dirs={'0.4.2':temp/'rebuilt-readers'}
        restore_notebook(dirs['0.4.2'],'0.4.2',retained['0.4.2'])
        # Restore source files at the inspected commit, so historical readers
        # are reproducible even after subsequent narrative amendments.
        for name in ('obligations','PARISH-QA-001-R1'):
            dest=temp/name;dest.mkdir()
            names = ('README.md','build_readers.py','sources.json','mappings.json','parish-test-plan.json','decision-record.json') if name=='obligations' else ('README.md','build_readers.py','evidence.json','reproduce.py')
            for filename in names:
                (dest/filename).write_bytes(git_bytes('scenario-batches/CB-001/'+name+'/'+filename))
        dirs['0.4.3']=temp/'v043';dirs['0.4.4']=temp/'v044'
        run(temp/'obligations/build_readers.py','--base',dirs['0.4.2'],'--out',dirs['0.4.3'])
        restore_notebook(dirs['0.4.3'],'0.4.3',retained['0.4.3'])
        run(temp/'PARISH-QA-001-R1/build_readers.py','--base',dirs['0.4.3'],'--out',dirs['0.4.4'])
        restore_notebook(dirs['0.4.4'],'0.4.4',retained['0.4.4'])
        for version in VERSIONS:
            dest=ROOT/'reading/editions'/f'{version}-draft';dest.mkdir(parents=True,exist_ok=True)
            records=[]
            for filename, expected in retained[version]['files'].items():
                data=(dirs[version]/filename).read_bytes()
                write_once(dest/filename,data)
                records.append(dict(path=str((dest/filename).relative_to(ROOT)),
                                    **expected, origin='matches_original_delivered_bytes'))
            notebook=dest/f'NodeNorm_Notebook_v{version.replace(".","_")}.ipynb'
            check=execute_copy(notebook) if execute else {'offline_replay_completed':False}
            entry={'files':records,'replay_check':check,'status':'draft_research_reading_snapshot'}
            if pdf:
                entry['pdf']=render_pdf(dest/f'NodeNorm_Study_v{version.replace(".","_")}.html',dest/f'NodeNorm_Study_v{version.replace(".","_")}.pdf')
            index['editions'][version+'-draft']=entry
        # The dependency archive is explicit about replay rather than rewriting the initial experiment.
        dependency=ROOT/'reading/archive-support/cir001/replay-inputs';dependency.mkdir(exist_ok=True)
        for filename in ('cases.json','registry.json','raw-results.replay.json','replay-receipt.json','case-results.csv'):
            write_once(dependency/filename,(replay/filename).read_bytes())
    index['root_readme_unchanged']=(REPO/'README.md').read_bytes()==baseline_readme
    (ROOT/'reading/ARTIFACT_INDEX.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'editions':len(index['editions']),'exact_original_text_and_notebook_files':12,
                      'offline_replays':execute,'pdf_renders':pdf,'root_readme_unchanged':True,
                      'research_calls':0,'canonical_or_scientific_approval':False},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--pdf',action='store_true')
    args=parser.parse_args()
    build(args.execute,args.pdf)
