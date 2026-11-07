"""Append OA-001 to the five existing 0.4.2 draft readers, offline.

Use --base pointing to the earlier portable CIR-001 reading package, which is
preserved unchanged. This is a draft export; no repository release is changed.
"""
from pathlib import Path
import argparse, hashlib, json
import mistune, nbformat

P=argparse.ArgumentParser()
P.add_argument('--base',type=Path,required=True)
P.add_argument('--out',type=Path,required=True)
P.add_argument('--execute',action='store_true')
P.add_argument('--pdf',action='store_true')
a=P.parse_args();R=Path(__file__).resolve().parent;out=a.out;out.mkdir(parents=True,exist_ok=True)
text=(R/'README.md').read_text(encoding='utf-8')
files=['sources.json','mappings.json','parish-test-plan.json','decision-record.json']
data={n.removesuffix('.json'):json.loads((R/n).read_text(encoding='utf-8')) for n in files}
render=mistune.create_markdown(escape=True,plugins=['table'])
css='''
.oa-card{padding:28px;border:1px solid var(--line,#ded7e8);border-radius:14px;background:white;margin:22px 0;overflow-wrap:anywhere}.oa-card h1{font-size:32px;line-height:1.25}.oa-card h2{font-size:25px;margin-top:32px}.oa-card h3{font-size:20px}.oa-card table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.5;margin:22px 0}.oa-card th,.oa-card td{padding:12px;border:1px solid #ddd7e8;text-align:left;vertical-align:top}.oa-card th{background:var(--lav,#eeebf8)}.oa-card summary{font-weight:650;cursor:pointer;padding:14px 0}.oa-scroll{overflow-x:auto}.oa-banner{background:var(--lav,#eeebf8);border:1px solid var(--line,#ded7e8);border-radius:12px;padding:20px;margin:22px 0;line-height:1.6}.oa-card a{overflow-wrap:anywhere}.oa-path{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:18px 0}.oa-path span{padding:15px;border:1px solid #d8d1e8;border-radius:8px;font-size:15px;background:white}.oa-small{font-size:14px;color:#625d70}@media(max-width:760px){.oa-card{padding:18px}.oa-card table{min-width:600px}.oa-path{grid-template-columns:repeat(2,1fr)}}@media print{.oa-card{padding:0;border:0;break-inside:auto}.oa-card h1,.oa-card h2,.oa-card h3{break-after:avoid;break-inside:avoid}.oa-card h1{font-size:23pt}.oa-card h2{font-size:18pt}.oa-card table{font-size:8pt;min-width:0!important;table-layout:fixed}.oa-card th,.oa-card td{padding:6px;overflow-wrap:anywhere}.oa-card tr{break-inside:avoid}.oa-scroll{overflow:visible}.oa-path{grid-template-columns:repeat(4,1fr)}.oa-path span{font-size:9pt;padding:10px}.oa-banner{font-size:10pt;padding:12px}.oa-card details{display:block}}
'''
html=lambda t:render(t).replace('<table>','<div class="oa-scroll"><table>').replace('</table>','</table></div>')
path='<div class="oa-path"><span>1. Right source?</span><span>2. Supported meaning?</span><span>3. Applicable here?</span><span>4. Control operated?</span></div>'
section='<section class="section" id="obligations"><div class="eyebrow">Institutional context · OA-001</div>'+path+'<details class="oa-card" open><summary>Canon law, responsibilities and the next parish-assistant packet</summary>'+html(text)+'</details></section>'
# Expected source files are explicit and are never overwritten.
needed=['NodeNorm_Study_v0_4_2.html','NodeNorm_Notebook_v0_4_2.ipynb','NodeNorm_Protocol_v0_4_2.html','NodeNorm_Protocol_v0_4_2.md']
for n in needed:
 if not (a.base/n).is_file():raise FileNotFoundError(a.base/n)
manifest={'reading_version':'0.4.3-draft','protocol_version':'0.3.0; unchanged and unfrozen','obligations_version':'0.1.0-draft','base':{n:hashlib.sha256((a.base/n).read_bytes()).hexdigest() for n in needed},'sources':{n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in files},'new_experimental_results':False,'qualified_review':'pending'}
s=(a.base/needed[0]).read_text()
s=s.replace('</style>',css+'</style>',1)
s=s.replace('<main>','<main><div class="oa-banner"><strong>Reading edition 0.4.3-draft.</strong> Five scenario-to-obligation mappings and a six-prompt parish-assistant packet are now documented. R1 is unchanged; no canonical approval or new model experiment is claimed. <a href="#obligations">Read the new chapter</a>.</div>',1)
s=s.replace('<section class="section" id="cir001-result">',section+'<section class="section" id="cir001-result">',1)
s=s.replace('<div class="navlinks">','<div class="navlinks"><a href="#obligations">Obligations</a>',1)
s=s.replace('<strong>Reading update 0.4.2-draft.</strong>','<strong>Prior engineering increment: 0.4.2-draft.</strong>',1)
(out/'NodeNorm_Study_v0_4_3.html').write_text(s)
p=(a.base/needed[3]).read_text()+'\n\n## Applicability supplement OA-001\n\nThis annex adds candidate sources, roles and a draft test packet. It does not freeze or retrospectively change the main protocol or the R1 experiment.\n\n'+text
(out/'NodeNorm_Protocol_v0_4_3.md').write_text(p)
ph=(a.base/needed[2]).read_text().replace('</style>',css+'</style>',1)
ph=ph.replace('</main>','<section class="oa-card" id="obligations">'+html('## Applicability supplement OA-001\n\nReading edition 0.4.3-draft. Core protocol 0.3.0 remains unchanged and unfrozen.\n\n'+text)+'</section></main>',1)
(out/'NodeNorm_Protocol_v0_4_3.html').write_text(ph)
nb=nbformat.read(a.base/needed[1],as_version=4)
nb.cells.insert(1,nbformat.v4.new_markdown_cell(text))
code="""# Embedded OA-001 records. No external requests or approval inference.
import json
OA = json.loads("""+repr(json.dumps(data,ensure_ascii=False))+""")
source_ids = {s['id'] for s in OA['sources']['sources']}
assert len(OA['mappings']['mappings']) == 5
for m in OA['mappings']['mappings']:
    assert set(m['source_ids']) <= source_ids
    assert m['assessment']['canonical_applicability'] == 'pending_qualified_review'
    assert m['assessment']['compliance_conclusion'] == 'not_assessed'
    assert m['assessment']['approval_record'] is None
print('10 source-page records; five candidate applicability mappings.')
print('No qualified review, compliance determination or ecclesial approval recorded.')
"""
nb.cells.insert(2,nbformat.v4.new_code_cell(code))
nb.cells.insert(3,nbformat.v4.new_code_cell("""# Inspect the six prospective prompts; this cell does not execute them.
packet = OA['parish-test-plan']
assert packet['run_count'] == 0 and packet['outputs'] == []
for c in packet['cases']:
    assert c['response'] is None
    print(c['id'], '(' + c['kind'] + '):', c['prompt'])
print('Prepared only. Specify the actual system and freeze the bounded run before execution.')
"""))
nb.metadata['oa001_update']=manifest
np=out/'NodeNorm_Notebook_v0_4_3.ipynb'
if a.execute:
 from nbclient import NotebookClient
 import tempfile
 with tempfile.TemporaryDirectory() as d:
  NotebookClient(nb,timeout=120,kernel_name='python3',resources={'metadata':{'path':d}}).execute()
nbformat.validate(nb);nbformat.write(nb,np)
if a.pdf:
 from playwright.sync_api import sync_playwright
 import shutil
 with sync_playwright() as pw:
  opts={'headless':True};exe=shutil.which('chromium') or shutil.which('chromium-browser')
  if exe:opts['executable_path']=exe
  browser=pw.chromium.launch(**opts);page=browser.new_page(viewport={'width':1440,'height':1000})
  page.set_content(s,wait_until='load');page.evaluate('document.querySelectorAll("details").forEach(x=>x.open=true)');page.emulate_media(media='print')
  page.pdf(path=str(out/'NodeNorm_Study_v0_4_3.pdf'),format='Letter',print_background=True,margin={'top':'16mm','bottom':'16mm','left':'13mm','right':'13mm'})
  browser.close()
manifest['reader_hashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('NodeNorm_*') if p.is_file()}
manifest['notebook_code_cells']=len([c for c in nb.cells if c.cell_type=='code'])
manifest['notebook_executed']=a.execute
(out/'READING_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Built the synchronized draft readers. No new study or model responses generated.')
