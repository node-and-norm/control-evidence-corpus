"""Append the live observation run to recovered 0.4.3 readers. Offline only."""
from pathlib import Path
import argparse,json,hashlib,html,tempfile,re
import mistune,nbformat
from nbclient import NotebookClient

p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--execute',action='store_true');p.add_argument('--pdf',action='store_true');a=p.parse_args()
R=Path(__file__).resolve().parent;O=a.out;O.mkdir(parents=True,exist_ok=True)
e=json.loads((R/'evidence.json').read_text());text=(R/'README.md').read_text();checker=(R/'reproduce.py').read_text().split("\nif __name__=='__main__':")[0]
draft=json.loads((R.parent/'obligations/parish-test-plan.json').read_text())
render=mistune.create_markdown(escape=True,plugins=['table'])
css='''
.pqa-panel{padding:26px;border:1px solid #dcd6e7;border-radius:14px;background:white;margin:22px 0;overflow-wrap:anywhere}.pqa-panel h1{font-size:32px}.pqa-panel h2{font-size:25px;margin-top:30px}.pqa-panel table{width:100%;font-size:14px;border-collapse:collapse;line-height:1.6}.pqa-panel td,.pqa-panel th{padding:12px;border:1px solid #dcd6e7;text-align:left;vertical-align:top}.pqa-panel th{background:#eeebf8}.pqa-overflow{overflow-x:auto}.pqa-banner{padding:22px;background:#eeebf8;border:1px solid #dcd6e7;border-radius:12px;margin:22px 0;line-height:1.65}.pqa-panel summary{font-weight:650;padding:14px 0;cursor:pointer}.pqa-response{padding:18px;border-left:3px solid #6c5bb8;background:#f7f5fb}.pqa-panel .small{font-size:14px;color:#615b6b}@media(max-width:700px){.pqa-panel{padding:18px}.pqa-panel table{min-width:580px}}@media print{.pqa-panel{padding:0;border:0;break-inside:auto}.pqa-panel h1{font-size:23pt}.pqa-panel h2{font-size:17pt;break-after:avoid}.pqa-panel table{font-size:8.3pt;min-width:0;table-layout:fixed}.pqa-panel td,.pqa-panel th{padding:6px;overflow-wrap:anywhere}.pqa-overflow{overflow:visible}.pqa-panel tr{break-inside:avoid}.pqa-records{display:none!important}.pqa-banner{font-size:10pt}.pqa-panel p{orphans:3;widows:3}}
'''
def safe_md(t):return render(t).replace('<table>','<div class="pqa-overflow"><table>').replace('</table>','</table></div>')
records=[]
for r in e['records']:
 refs=''.join('<li>'+html.escape(x['document_title'])+' · '+html.escape(x['document_reference'])+' · <a href="'+html.escape(x['source_url'],quote=True)+'">returned locator</a></li>' for x in r['response']['references'])
 records.append('<details class="pqa-panel pqa-records"><summary>'+r['case_id']+' · Exact prompt and captured service response</summary><p class="small">Generated service output. Unadjudicated; not endorsed advice. References are returned metadata, not independently verified sources.</p><h3>Submitted prompt</h3><p>'+html.escape(r['prompt']).replace('\n','<br>')+'</p><h3>Captured answer</h3><div class="pqa-response">'+safe_md(r['response']['answer'])+'</div><h3>Returned references</h3><ol>'+refs+'</ol></details>')
section='<section class="section" id="live-parish-run"><div class="eyebrow">Executed observation · PARISH-QA-001-R1</div><div class="pqa-panel">'+safe_md(text)+'</div><p class="small">Complete responses and reference metadata follow in HTML and the notebook; the PDF summarizes the run. The evidence JSON in the package retains all six records.</p>'+''.join(records)+'</section>'
s=(a.base/'NodeNorm_Study_v0_4_3.html').read_text()
assert re.search(r'<main\b[^>]*>',s) and 'id="obligations"' in s
s=s.replace('</style>',css+'</style>',1)
s=re.sub(r'(<main\b[^>]*>)',r'\1<div class="pqa-banner"><strong>Current reading edition 0.4.4-draft.</strong> The six-question live service observation is complete: six responses, no retries, qualified review pending. Earlier chapters remain dated records. <a href="#live-parish-run">Read the observations</a>.</div>',s,count=1)
s=s.replace('<section class="section" id="obligations">',section+'<section class="section" id="obligations">',1)
s=s.replace('<div class="navlinks">','<div class="navlinks"><a href="#live-parish-run">Live responses</a>',1)
s=s.replace('<strong>Reading edition 0.4.3-draft.</strong>','<strong>Earlier obligations snapshot: 0.4.3-draft.</strong>',1)
(O/'NodeNorm_Study_v0_4_4.html').write_text(s)
protocol=(a.base/'NodeNorm_Protocol_v0_4_3.md').read_text()+'\n\n## PARISH-QA-001-R1 observation annex\n\nReading edition 0.4.4-draft. Core comparison protocol 0.3.0 remains unfrozen and unchanged. The following run fixes a bounded observation procedure; it supplies no canonical or semantic correctness adjudication.\n\n'+text
(O/'NodeNorm_Protocol_v0_4_4.md').write_text(protocol)
ph=(a.base/'NodeNorm_Protocol_v0_4_3.html').read_text().replace('</style>',css+'</style>',1)
ph=ph.replace('</main>','<section class="pqa-panel" id="live-parish-run">'+safe_md('## Current observation annex · 0.4.4-draft\n\n'+text)+'</section></main>',1)
(O/'NodeNorm_Protocol_v0_4_4.html').write_text(ph)
nb=nbformat.read(a.base/'NodeNorm_Notebook_v0_4_3.ipynb',as_version=4)
nb.cells.insert(1,nbformat.v4.new_markdown_cell('# Current continuation: six service responses\n\nReading edition **0.4.4-draft**. The preceding draft question packet is preserved as a historical object. The actual executed run and its evidence are shown here. Source and semantic correctness remain unadjudicated. All code is offline.\n\n'+text))
code='import json\nPQA = json.loads('+repr(json.dumps(e,ensure_ascii=False))+')\nPQA_DRAFT = json.loads('+repr(json.dumps(draft,ensure_ascii=False))+')\n'+checker.replace('ROOT=Path(__file__).resolve().parent','ROOT=Path.cwd()')+'\nPQA_CHECK = check(PQA,PQA_DRAFT)\nprint(json.dumps(PQA_CHECK,indent=2))\n'
nb.cells.insert(2,nbformat.v4.new_code_cell(code))
for i,r in enumerate(e['records']):
 source='## Captured service output: '+r['case_id']+'\n\n**Unadjudicated generated output, not a verified finding.**\n\n### Exact prompt\n\n'+r['prompt']+'\n\n### Answer returned\n\n'+r['response']['answer']+'\n\n### Returned references\n\n'+'\n'.join('- '+x['document_title']+' · '+x['document_reference']+' · '+x['source_url'] for x in r['response']['references'])
 nb.cells.insert(3+i,nbformat.v4.new_markdown_cell(source))
nb.metadata['parish_observation']={'reading_version':'0.4.4-draft','run_id':e['run_id'],'freeze_commit':e['freeze_commit'],'evidence_sha256':hashlib.sha256((R/'evidence.json').read_bytes()).hexdigest(),'network_required':False,'qualified_review':'pending'}
if a.execute:
 with tempfile.TemporaryDirectory() as d:NotebookClient(nb,timeout=120,kernel_name='python3',resources={'metadata':{'path':d}}).execute()
nbformat.validate(nb);nbformat.write(nb,O/'NodeNorm_Notebook_v0_4_4.ipynb')
if a.pdf:
 from playwright.sync_api import sync_playwright
 import shutil
 with sync_playwright() as pw:
  opts={'headless':True};exe=shutil.which('chromium') or shutil.which('chromium-browser')
  if exe:opts['executable_path']=exe
  browser=pw.chromium.launch(**opts);page=browser.new_page(viewport={'width':1440,'height':1000})
  page.set_content(s,wait_until='load');page.evaluate('document.querySelectorAll("details").forEach(x=>x.open=true)');page.emulate_media(media='print')
  page.pdf(path=str(O/'NodeNorm_Study_v0_4_4.pdf'),format='Letter',print_background=True,margin={'top':'16mm','bottom':'16mm','left':'13mm','right':'13mm'})
  browser.close()
manifest={'reading_edition':'0.4.4-draft','core_protocol':'0.3.0 unchanged/unfrozen','evidence_sha256':hashlib.sha256((R/'evidence.json').read_bytes()).hexdigest(),'base_files':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in a.base.glob('NodeNorm_*') if x.suffix in {'.html','.md','.ipynb'}},'readers':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in O.glob('NodeNorm_*')},'notebook_code_cells':sum(c.cell_type=='code' for c in nb.cells),'notebook_executed':a.execute,'rendered_pdf':a.pdf,'new_service_calls':0,'independent_review':False}
(O/'READING_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Built five readers. Offline construction; no new service calls.')
