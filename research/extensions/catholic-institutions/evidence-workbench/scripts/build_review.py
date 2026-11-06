#!/usr/bin/env python3
"""Build a read-first HTML guide and self-contained notebook. No network calls.

Narrative source: EVIDENCE_REVIEW.md. Evidence source: evidence-inventory.json.
Generated notebook snapshots are labeled and preserve original artifact hashes.
"""
from __future__ import annotations
from pathlib import Path
from html import escape
import hashlib
import json
import re
import importlib.metadata
import mistune

ROOT=Path(__file__).resolve().parent.parent
TEXT=(ROOT/'EVIDENCE_REVIEW.md').read_text(encoding='utf-8')
INVENTORY=json.loads((ROOT/'evidence-inventory.json').read_text(encoding='utf-8'))
CHECKER=(ROOT/'scripts/check_evidence.py').read_text(encoding='utf-8')
MD=mistune.create_markdown(escape=True, plugins=['table'])
chapters=re.split(r'(?m)^## (?=\d\d\. )', TEXT)
head=chapters[0]
parts=[]
for piece in chapters[1:]:
 title,body=piece.split('\n',1)
 num=title[:2]
 parts.append((num,title,body.strip()))

CSS='''
:root{--paper:#f8f7f3;--ink:#24232b;--muted:#625d6e;--line:#dcd7e4;--accent:#5544b5;--wash:#eeebf8;--warn:#79531b;--white:#fff;--dark:#252030}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:86px}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}a{color:var(--accent);text-underline-offset:3px;overflow-wrap:anywhere}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid #ad8e30;outline-offset:4px}.skip{position:absolute;left:-999px}.skip:focus{left:20px;top:15px;background:white;z-index:20;padding:10px}header{position:sticky;top:0;background:rgba(248,247,243,.97);z-index:10;border-bottom:1px solid var(--line)}nav{max-width:1220px;margin:auto;padding:17px 32px;display:flex;gap:24px;align-items:center;justify-content:space-between}.brand{font-weight:750;font-size:20px}.nav-links{display:flex;gap:23px;font-size:14px;align-items:center}.nav-links a{text-decoration:none}main{max-width:1160px;margin:auto;padding:0 32px 70px}.hero{padding:67px 0 36px;display:grid;grid-template-columns:1.6fr 1fr;gap:48px}.eyebrow{text-transform:uppercase;letter-spacing:.13em;font-weight:750;font-size:12px;color:var(--accent)}h1{font-size:clamp(38px,5vw,64px);line-height:1.06;letter-spacing:-2.5px;margin:14px 0 24px;max-width:700px}.lede{font-size:21px;line-height:1.6;max-width:720px;color:#504858}.hero-aside{align-self:center;border-left:3px solid var(--accent);padding:18px 0 18px 25px;font-size:17px}.hero-aside p{margin:8px 0}.small{font-size:14px;color:var(--muted)}.status{background:var(--wash);border:1px solid #d6cfee;border-radius:12px;padding:20px 24px}.status strong{display:block;color:var(--accent);margin-bottom:5px}.stats{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);border-radius:14px;background:white;margin:26px 0 35px;overflow:hidden}.stat{padding:23px;border-right:1px solid var(--line)}.stat:last-child{border:0}.stat b{font-size:31px;color:var(--accent);display:block}.stat span{font-size:14px;line-height:1.5;display:block}.stat small{font-size:12px;color:var(--muted);display:block;margin-top:7px}.intro{padding:24px 0 26px}h2{font-size:30px;line-height:1.25;letter-spacing:-.5px}h3{font-size:22px;line-height:1.4}.routes{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin:22px 0}.route{background:white;border:1px solid var(--line);border-radius:13px;padding:22px}.route h3{font-size:18px;margin:0 0 8px}.route p{font-size:15px;margin:0}.chain{display:grid;grid-template-columns:repeat(6,1fr);gap:9px;margin:22px 0 36px}.chain div{border:1px solid var(--line);background:white;border-radius:10px;padding:16px 12px;line-height:1.35}.chain small{color:var(--accent);font-weight:700;display:block;margin-bottom:8px}.chain b{font-size:15px}.toolbar{display:flex;flex-wrap:wrap;gap:9px;align-items:center;justify-content:space-between;margin:25px 0 18px}.toolbar div{display:flex;gap:9px;flex-wrap:wrap}button{font:inherit;font-size:14px;border:1px solid var(--line);background:white;color:var(--ink);padding:9px 15px;border-radius:8px;cursor:pointer}.chapter{border:1px solid var(--line);border-radius:13px;background:white;margin:13px 0;scroll-margin-top:90px}.chapter summary{cursor:pointer;padding:24px;list-style:none;display:flex;align-items:center;gap:16px;line-height:1.4}.chapter summary::-webkit-details-marker{display:none}.chapter summary:after{content:'+';margin-left:auto;color:var(--accent);font-size:25px}.chapter[open] summary:after{content:'−'}.chapter summary .n{color:var(--accent);font-size:14px;font-weight:750;min-width:25px}.chapter summary .title{font-size:20px;font-weight:680}.body{padding:0 27px 24px;max-width:100%;overflow-wrap:break-word}.body p{max-width:940px}.body p:first-child{margin-top:0}.table-wrap{overflow-x:auto;margin:20px 0}table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.55;margin:18px 0}th{text-align:left;background:var(--wash);font-weight:700}th,td{padding:13px 14px;border:1px solid var(--line);vertical-align:top}td:first-child{font-weight:620;width:22%}code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;background:#f0edf5;padding:2px 4px;border-radius:4px;font-size:.86em;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f1f7;padding:20px;border-radius:8px;font-size:12px;line-height:1.5}li{margin:8px 0}footer{padding-top:35px;margin-top:40px;border-top:1px solid var(--line);font-size:13px;color:var(--muted)}.ending{background:var(--dark);color:white;border-radius:14px;padding:32px;margin-top:35px}.ending h2{margin:0 0 14px}.ending p{margin:8px 0;color:#e3deec}.not-live{font-size:13px;color:var(--muted);padding:14px 0}.print-note{display:none}
@media(max-width:760px){nav{padding:15px 20px;align-items:flex-start;gap:12px;flex-direction:column}.nav-links{gap:16px;font-size:13px;flex-wrap:wrap}main{padding:0 20px 40px}.hero{grid-template-columns:1fr;gap:20px;padding-top:36px}h1{letter-spacing:-1.5px}.hero-aside{font-size:16px}.stats{grid-template-columns:repeat(2,1fr)}.stat:nth-child(2){border-right:0}.stat:nth-child(-n+2){border-bottom:1px solid var(--line)}.routes{grid-template-columns:1fr}.chain{grid-template-columns:repeat(2,1fr)}.chapter summary{padding:19px 16px;gap:10px}.chapter summary .title{font-size:18px}.body{padding:0 17px 20px}.lede{font-size:19px}h2{font-size:26px}}
@media print{@page{size:Letter;margin:18mm 15mm}body{background:white;font-size:10pt;line-height:1.5}header,.toolbar,.skip{display:none}main{padding:0;max-width:none}.hero{padding:0 0 16px;gap:20px}h1{font-size:32pt;letter-spacing:-1px}.lede{font-size:13pt}.hero-aside{font-size:10pt}.status{padding:12px;font-size:9pt}.stats{margin:15px 0}.stat{padding:12px}.stat b{font-size:23pt}.stat span{font-size:9pt}.stat small{font-size:8pt}.route{padding:12px}.routes{gap:8px}.route p{font-size:9pt}.route h3{font-size:11pt}.chain{gap:5px}.chain div{padding:10px}.chain b{font-size:9pt}.chapter{border:none;border-top:1px solid #bbb;border-radius:0;margin:15px 0;break-inside:auto}.chapter summary{padding:14px 0 9px;break-after:avoid}.chapter summary .title{font-size:15pt}.chapter summary:after{display:none}.chapter .body{display:block;padding:0}h2,h3{break-after:avoid}.chapter p{orphans:3;widows:3}table{font-size:8.5pt;line-height:1.4;table-layout:fixed}th,td{padding:7px;overflow-wrap:anywhere}tr{break-inside:avoid}pre,code{font-size:8pt}a{color:#39314b}.ending{background:white;border:1px solid #aaa;color:var(--ink);padding:18px;break-inside:avoid}.ending p{color:var(--ink)}footer{display:none}.print-note{display:block;font-size:9pt}.not-live{font-size:8pt}.table-wrap{overflow:visible}}
'''

def render_body(text: str)->str:
 return MD(text).replace('<table>','<div class="table-wrap"><table>').replace('</table>','</table></div>')

def build_html()->str:
 panels=[]
 for n,title,body in parts:
  panels.append(f'<details class="chapter" id="chapter-{n}" {"open" if n in {"01","03"} else ""}><summary><span class="n">{n}</span><span class="title">{escape(title[4:])}</span></summary><div class="body">{render_body(body)}</div></details>')
 stats=[('18','Normative mapping candidates','All await qualified review'),('6','Selected locator comparisons','Legacy summaries, not all calls'),('0','Catholic safeguard studies completed','Source-package declared status'),('17','Software boundary tests','Synthetic fixtures, not research results')]
 stat_html=''.join(f'<div class="stat"><b>{a}</b><span>{b}</span><small>{c}</small></div>' for a,b,c in stats)
 chain=''.join(f'<div><small>{i:02}</small><b>{x}</b></div>' for i,x in enumerate(['Question & plan','Source & passage','Interpretation & context','Test & observation','Review & disagreement','Finding & release'],1))
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Node &amp; Norm | Follow the evidence</title><style>{CSS}</style></head><body><a class="skip" href="#main">Skip to study</a><header><nav><span class="brand">Node &amp; Norm</span><div class="nav-links"><a href="#start">Start here</a><a href="#chapter-03">Evidence audit</a><a href="#chapter-05">Worked case</a><a href="#chapter-10">Next gates</a></div></nav></header><main id="main"><section class="hero" id="start"><div><div class="eyebrow">Catholic institutional AI study · Evidence companion</div><h1>Follow the evidence.</h1><p class="lede">From a source to a finding, with every interpretation, limitation, and review made visible.</p></div><aside class="hero-aside"><strong>Designed for scrutiny.</strong><p>Read the study without code. Open the detailed record when a claim needs closer examination.</p><span class="small">Evidence workbench 0.3.0<br>6 November 2026</span></aside></section><div class="status"><strong>A reviewable method, not a completed empirical study.</strong>The pilot protocol remains the unfrozen 0.2.0 draft. This companion adds an evidence audit and prospective recording requirements. It leaves the existing study and its Catholic source mappings intact.</div><div class="stats">{stat_html}</div><div class="not-live">Static, versioned snapshot. No live data feed, model calls, or automatic approval. Prior missing evidence is explicitly identified.</div><section class="intro"><div class="eyebrow">Choose a reading path</div><h2>One study. Different questions.</h2><div class="routes"><div class="route"><h3>Institutional leaders</h3><p>What is supported? What remains unknown? Start with sections 01, 03, 05 and 10.</p></div><div class="route"><h3>Theologians &amp; Catholic reviewers</h3><p>Where does the source end and our inference begin? Read sections 04, 05, 07 and 09.</p></div><div class="route"><h3>Research &amp; technical reviewers</h3><p>Can the method be challenged and repeated? Read sections 02, 06, 08 and 11.</p></div></div><div class="chain" aria-label="Evidence sequence">{chain}</div></section><div class="toolbar"><strong>The guided study</strong><div><button type="button" id="open-all">Expand all sections</button><button type="button" id="close-all">Collapse sections</button><button type="button" id="print">Print / PDF</button></div></div><p class="print-note">Reading copy: all sections expanded. The notebook and machine-readable records remain the reproducibility companion.</p>{''.join(panels)}<section class="ending"><div class="eyebrow" style="color:#d6caff">Next evidence gate</div><h2>Capture a small run completely.</h2><p>Preserve the source requests, returned passages, mismatches, decisions and review status. Then invite qualified scrutiny of a bounded set of mappings.</p><p>More agents and more prose are useful only when they improve the evidence.</p></section><footer>Node &amp; Norm · CEC Catholic institutional extension<br>Reader sources: EVIDENCE_REVIEW.md and evidence-inventory.json. No independent approval or institutional endorsement is implied.</footer></main><script>const ds=()=>document.querySelectorAll('details.chapter');document.getElementById('open-all').onclick=()=>ds().forEach(d=>d.open=true);document.getElementById('close-all').onclick=()=>ds().forEach(d=>d.open=false);document.getElementById('print').onclick=()=>{{ds().forEach(d=>d.open=true);window.print();}};document.querySelectorAll('a[href^="#chapter-"]').forEach(a=>a.addEventListener('click',()=>{{document.querySelector(a.getAttribute('href')).open=true;}}));window.addEventListener('beforeprint',()=>ds().forEach(d=>d.open=true));</script></body></html>'''

def cell(kind,text,idx):
 out={'cell_type':kind,'id':f'{kind}-{idx:02d}','metadata':{},'source':text.splitlines(keepends=True)}
 if kind=='code':out.update(execution_count=None,outputs=[])
 return out

def build_notebook():
 c=[]
 c.append(cell('markdown','# Follow the evidence\n\n**Node & Norm | Evidence workbench 0.3.0 | 6 November 2026**\n\nRead the text first. The optional code runs offline using an embedded snapshot. No API key, paid model, Magisterium call, or connection to the live repository is required. The governing pilot protocol remains the unfrozen 0.2.0 draft. Software checks below are not empirical safeguard tests.\n\nEach section has the same numbering as the HTML guide. The underlying source maps remain in the original study package.',0))
 for n,title,body in parts:
  c.append(cell('markdown','## '+title+'\n\n'+body,int(n)))
  if n=='03':
   code='''# Frozen artifact inventory, embedded for portable offline reading.
# These are retained summaries, not complete raw historical tool responses.
import json
from collections import Counter
SNAPSHOT = json.loads('''+repr(json.dumps(INVENTORY,ensure_ascii=False))+''')
counts = Counter(row['classification'] for row in SNAPSHOT['locator_comparisons'])
print('Normative candidates:', len(SNAPSHOT['mapping_candidates']))
print('Selected locator comparisons:', len(SNAPSHOT['locator_comparisons']))
print('Row classifications:', dict(sorted(counts.items())))
print('Independent human reviews recorded:', SNAPSHOT['independent_human_reviews_recorded'])
print('Counts are artifact inventory only; no general reliability estimate.')
'''
   c.append(cell('code',code,31))
  if n=='05':
   c.append(cell('code',"# Inspect the worked comparison; do not silently repair its locator.\nrow = next(x for x in SNAPSHOT['locator_comparisons'] if x['id'] == 'LOC-04')\nfor key in ['id', 'document', 'search_expected_ref', 'fetch_returned_ref', 'classification']:\n    print(f'{key}: {row[key]}')\nprint('Raw original tool capture: absent from inspected v0.2 package.')\n",51))
  if n=='08':
   c.append(cell('markdown','### Optional executable boundary checks\n\nThe following code is the exact local `scripts/check_evidence.py` implementation with its command-line entry point omitted. All fixture people and observations are invented. Passing checks establish software behavior for these examples only. Empty blocker lists never authorize publication.',81))
   test_code=CHECKER.split("\nif __name__ == '__main__':")[0]
   # Keep future import first in the cell, as required by Python.
   c.append(cell('code',test_code+'\n\nMAINTENANCE_RESULT = run_checks()\nprint(json.dumps(MAINTENANCE_RESULT, indent=2))\nassert MAINTENANCE_RESULT["success"]\n',82))
  if n=='11':
   code='''# Optional byte correspondence check. This never queries GitHub.
from pathlib import Path
candidate_roots = [Path.cwd(), Path.cwd().parent]
matching_root = next((p for p in candidate_roots if (p/'study.json').is_file() and (p/'data/normative-crosswalk.json').is_file()), None)
if matching_root is None:
    print('Companion study files absent: using embedded snapshot. No live or local-source verification claimed.')
else:
    mismatches = verify_hashes(matching_root, SNAPSHOT)
    print('Checked legacy package at:', matching_root.name)
    print('Hash mismatches:', mismatches)
    assert not mismatches, 'Legacy inputs differ; investigate before comparing versions.'
print('Replay of stored summaries is distinct from re-running model or retrieval calls.')
'''
   c.append(cell('code',code,111))
 return {'cells':c,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.11'},'node_norm':{'companion_version':'0.3.0','protocol_version':'0.2.0','evidence_status':'development_and_legacy_summary_only','network_required':False,'narrative_sha256':hashlib.sha256(TEXT.encode()).hexdigest(),'inventory_sha256':hashlib.sha256((ROOT/'evidence-inventory.json').read_bytes()).hexdigest()}},'nbformat':4,'nbformat_minor':5}

if __name__=='__main__':
 (ROOT/'evidence-review.html').write_text(build_html(),encoding='utf-8')
 (ROOT/'evidence-review.ipynb').write_text(json.dumps(build_notebook(),indent=1,ensure_ascii=False)+'\n',encoding='utf-8')
 print('Built evidence-review.html and evidence-review.ipynb from shared sources. No research or API calls executed.')
