#!/usr/bin/env python3
"""Build the reader-first HTML report and Jupyter study guide from study.json.

Design status only. No network, model inference, source ingestion, or empirical validation.
Uses Python 3.11+ standard library. Read PROTOCOL.md for method decisions.
"""
from __future__ import annotations
from pathlib import Path
from html import escape
from datetime import datetime, timezone
from urllib.parse import urlparse
from xml.sax.saxutils import escape as svg_escape
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent.parent
STUDY = json.loads((ROOT / 'study.json').read_text(encoding='utf-8'))
PROTOCOL = (ROOT / 'PROTOCOL.md').read_text(encoding='utf-8')
CROSSWALK = json.loads((ROOT / 'data/normative-crosswalk.json').read_text(encoding='utf-8'))
SOURCE_AUDIT = json.loads((ROOT / 'data/magisterium-locator-audit.json').read_text(encoding='utf-8'))


def e(x): return escape(str(x), quote=True)
def cells(items, key='name', value='question'):
    return ''.join(f'<div class="kv"><span>{e(it.get(key,""))}</span><strong>{e(it.get(value,""))}</strong></div>' for it in items)
def p(x): return f'<p>{e(x)}</p>'
def render_metric(m):
    return f'<div class="metric"><div class="metric-number">{e(m["value"])}</div><div class="metric-title">{e(m["label"])}</div><div class="metric-note">{e(m["note"])}</div></div>'
def render_hyp(h):
    return f'''<article class="hypothesis" id="{e(h['id'])}"><div class="hypo-top"><span class="hypo-id">{e(h['id'])}</span><span class="lozenge">{e(h['category'])}</span></div><h3>{e(h['title'])}</h3><p>{e(h['claim'])}</p><div class="hypo-detail"><div><b>How we would measure it</b><p>{e(h['measure'])}</p></div><div><b>What could challenge it</b><p>{e(h['challenge'])}</p></div></div></article>'''
def render_step(item):
    return f'''<article class="process-step"><div class="process-index">{e(item['number'])}</div><div class="process-content"><h3>{e(item['title'])}</h3><span class="mini-label">{e(item['subtitle'])}</span><p>{e(item['description'])}</p><small>{e(item['status'])}</small></div></article>'''
def render_stage(stage):
    state = stage['state']
    status = {'in_progress':'Design in progress', 'waiting':'Waiting for ingestion', 'planned':'Planned', 'deferred':'Deferred'}[state]
    lis = ''.join(f'<li>{e(x)}</li>' for x in stage['actions'])
    return f'''<details class="stage" data-state="{e(state)}" {'open' if stage['n']=='00' else ''}>
      <summary><span class="stage-n">{e(stage['n'])}</span><span class="stage-title"><strong>{e(stage['name'])}</strong><small>{e(stage['subtitle'])}</small></span><span class="state state-{e(state)}">{status}</span></summary>
      <div class="stage-body"><div><h4>Work to complete</h4><ul>{lis}</ul></div><div class="stage-outcome"><h4>Research output</h4><p>{e(stage['deliverable'])}</p><h4>Evidence gate</h4><p>{e(stage['gate'])}</p><h4>Dependency</h4><p>{e(stage['dependency'])}</p></div></div>
      </details>'''
def render_source(s):
    url=s['url']; assert urlparse(url).scheme=='https'
    return f'<li><div><a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(s["label"])}</a><span>{e(s["kind"])}</span></div><span class="external" aria-hidden="true">↗</span></li>'

def render_normative_item(item):
    dims = ', '.join(item['cec_dimensions'])
    return f'''<details class="norm-item"><summary><span><b>§{e(item['paragraph'])}</b> {e(item['proposed_concept'])}</span><span class="norm-tag">Review pending</span></summary><div class="norm-item-body"><p><strong>Research question</strong><br>{e(item['candidate_evidence_question'])}</p><p><strong>Potential CEC dimensions</strong><br><code>{e(dims)}</code></p><p class="small-note">Researcher proposal, not an official Catholic control requirement or a validated evaluation.</p><a href="{e(item['official_url'])}" target="_blank" rel="noopener noreferrer">Open authoritative Vatican publication</a></div></details>'''

def render_source_groups():
    groups=[]
    for document in CROSSWALK['source_documents']:
        candidates=[x for x in CROSSWALK['records'] if x['document_id']==document['id']]
        rows=''.join(render_normative_item(x) for x in candidates)
        groups.append(f'''<article class="norm-group"><div class="norm-head"><span class="eyebrow">{e(document['issuer'])}</span><h3>{e(document['title'])}</h3><p>{e(document['source_date'])} · {len(candidates)} development mappings</p><a href="{e(document['official_url'])}" target="_blank" rel="noopener noreferrer">Read the official document</a></div><div class="norm-rows">{rows}</div></article>''')
    return ''.join(groups)

CSS = r'''
:root{--bg:#f7f6f3;--paper:#fff;--ink:#1c1923;--muted:#5f5b67;--line:#dedbe4;--purple:#5145cd;--lav:#eeecff;--deep:#191820;--green:#3b633d;--amber:#88651c;--quiet:#eeece8;--shadow:0 16px 36px rgba(30,24,55,.055)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{background:var(--bg);color:var(--ink);margin:0;font:17px/1.62 system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}a{color:var(--purple);text-underline-offset:3px}a:hover{text-decoration-thickness:2px}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid var(--purple);outline-offset:4px}img{max-width:100%}
.topbar{background:var(--deep);color:white;position:sticky;z-index:12;top:0;box-shadow:0 2px 18px rgba(0,0,0,.1)}.nav{max-width:1260px;margin:0 auto;padding:15px 32px;display:flex;justify-content:space-between;align-items:center;gap:20px}.brand{color:white;text-decoration:none;font-weight:790;letter-spacing:-.5px;font-size:21px}.brand-dot{color:#c2baff}.navlinks{display:flex;gap:20px;align-items:center;flex-wrap:wrap}.navlinks a{color:#e9e8f3;text-decoration:none;font-size:13px}.navlinks a:hover{color:white;text-decoration:underline}
main{max-width:1260px;padding:0 32px 90px;margin:0 auto}.eyebrow{text-transform:uppercase;letter-spacing:2.1px;font-weight:780;color:var(--purple);font-size:12px}.hero{display:grid;grid-template-columns:1.55fr .85fr;gap:60px;align-items:center;padding:72px 0 44px}.hero h1{font-size:clamp(43px,5.4vw,75px);font-weight:750;line-height:1.05;letter-spacing:-3.3px;margin:13px 0 24px;color:var(--purple);max-width:820px}.hero p{font-size:21px;color:#484450;max-width:760px;margin:0 0 22px}.hero-actions{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.button-link{padding:10px 16px;border:1px solid var(--purple);border-radius:8px;text-decoration:none;font-size:14px;font-weight:720}.button-link.primary{color:#fff;background:var(--purple)}.button-link.secondary{background:white}.hero-aside{border-left:3px solid var(--purple);padding:7px 0 7px 24px}.hero-aside h2{margin:0 0 12px;font-size:24px;line-height:1.3}.hero-aside p{font-size:17px;line-height:1.6;margin:0}.hero-aside small{display:block;font-size:13px;color:var(--muted);margin-top:17px}
.strip{border-block:1px solid var(--line);display:flex;justify-content:space-between;gap:15px;padding:15px 0;color:var(--muted);font-size:13px;flex-wrap:wrap}.strip b{color:#38333e}.section{padding-top:70px;scroll-margin-top:70px}.section-head{display:flex;justify-content:space-between;align-items:end;gap:28px}.section h2{font-size:clamp(28px,3.8vw,39px);line-height:1.19;letter-spacing:-1.4px;margin:10px 0 16px}.section .intro{max-width:840px;color:var(--muted);font-size:18px}.small-note{color:var(--muted);font-size:13px}.thin-rule{border:0;border-top:1px solid var(--line);margin:26px 0}.metric-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:23px}.metric{background:white;border:1px solid var(--line);border-radius:13px;padding:24px;min-height:164px}.metric-number{font-size:32px;line-height:1.15;letter-spacing:-1.3px;font-weight:730;margin-bottom:12px}.metric-title{font-size:15px;font-weight:720}.metric-note{font-size:13px;color:var(--muted);line-height:1.4;margin-top:7px}.target-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:20px}.target{background:#efedff;border:1px solid #ded9fc;border-radius:12px;padding:19px 23px}.target strong{display:block;color:#30258f;font-size:30px;line-height:1.2}.target b{display:block;font-size:15px;margin:7px 0 3px}.target small{color:#5a5472;font-size:12px}
.hero-note{border-left:3px solid var(--purple);padding:14px 22px;background:#f0eeff;border-radius:0 10px 10px 0;margin-top:27px;font-size:16px}.hero-note p{margin:0}.two-cols{display:grid;grid-template-columns:1.4fr .8fr;gap:26px;margin-top:24px}.question-panel{background:var(--deep);border-radius:16px;padding:30px;color:#fff}.question-panel .eyebrow{color:#beb8ff}.question-panel p{font-size:23px;line-height:1.5;letter-spacing:-.3px;margin:16px 0}.contrast{border:1px solid var(--line);border-radius:14px;background:#fff;padding:26px}.contrast h3{font-size:19px;margin:0 0 10px}.contrast p{margin:0;color:var(--muted);font-size:16px}
.segment{display:flex;gap:8px;flex-wrap:wrap;margin:25px 0 12px}.segment button,.controls button{border:1px solid #c5bfdb;border-radius:8px;background:white;color:#493db6;cursor:pointer;padding:9px 14px;font:650 14px system-ui}.segment button[aria-selected="true"]{background:var(--purple);color:white;border-color:var(--purple)}.audience-panel{border:1px solid var(--line);background:#fff;padding:22px 26px;border-radius:13px;min-height:125px}.audience-panel h3{font-size:19px;margin:0 0 6px}.audience-panel p{color:var(--muted);margin:0}
.hypotheses{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:17px;margin-top:25px}.hypothesis{background:white;border:1px solid var(--line);border-radius:14px;padding:27px}.hypo-top{display:flex;justify-content:space-between;align-items:center;gap:15px}.hypo-id{font-size:13px;font-weight:800;color:var(--purple)}.lozenge{font-size:11px;padding:4px 10px;background:var(--lav);color:#443c9e;border-radius:30px;font-weight:710}.hypothesis h3{font-size:21px;letter-spacing:-.4px;margin:17px 0 11px}.hypothesis>p{color:#484451;font-size:16px}.hypo-detail{display:grid;grid-template-columns:1fr 1fr;gap:20px;border-top:1px solid var(--line);margin-top:19px;padding-top:17px}.hypo-detail b{font-size:12px;text-transform:uppercase;letter-spacing:1px;color:var(--purple)}.hypo-detail p{font-size:14px;line-height:1.5;color:var(--muted);margin:8px 0 0}
.flow-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:26px}.process-step{min-height:198px;border:1px solid var(--line);border-radius:13px;background:white;padding:20px;position:relative}.process-index{color:var(--purple);font-weight:800;font-size:12px;letter-spacing:1px}.process-content h3{font-size:23px;margin:8px 0 0;letter-spacing:-.5px}.mini-label{font-size:13px;color:var(--purple);font-weight:650}.process-content p{font-size:15px;color:#514c58;margin:11px 0}.process-content small{color:var(--muted);font-size:12px}.flow-caption{font-size:13px;color:var(--muted);margin-top:13px}
.objects-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:20px}.object{border:1px solid var(--line);border-radius:11px;padding:19px;background:white}.object small{font-size:12px;color:var(--purple);font-weight:760}.object h3{font-size:18px;margin:5px 0 7px}.object p{font-size:15px;color:var(--muted);margin:0}.case{border:1px solid #d5d0e5;border-radius:17px;background:#fff;padding:26px;margin-top:24px}.case-header{display:flex;gap:10px;justify-content:space-between;align-items:center;flex-wrap:wrap}.case h3{font-size:23px;margin:0}.case-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:22px}.case-cell{border-top:1px solid var(--line);padding-top:13px}.case-cell b{font-size:12px;color:var(--purple);text-transform:uppercase;letter-spacing:.7px}.case-cell p{font-size:15px;margin:6px 0;color:#4c4754}
.controls{display:flex;gap:9px;flex-wrap:wrap}.stages{margin-top:22px;border-top:1px solid var(--line)}details.stage{border-bottom:1px solid var(--line)}.stage summary{cursor:pointer;list-style:none;display:grid;grid-template-columns:43px 1fr auto 20px;gap:20px;align-items:center;padding:22px 4px}.stage summary::-webkit-details-marker{display:none}.stage summary:after{content:'+';color:var(--purple);font-size:24px;grid-column:4;grid-row:1}.stage[open] summary:after{content:'−'}.stage-n{font-size:14px;font-weight:760;color:var(--purple);border:1px solid #c7c0ee;border-radius:50%;height:41px;width:41px;display:flex;align-items:center;justify-content:center}.stage-title{display:flex;flex-direction:column;gap:4px;padding-right:20px}.stage-title strong{font-size:20px;line-height:1.3}.stage-title small{color:var(--muted);font-size:14px}.state{font-size:11px;font-weight:740;padding:5px 10px;border-radius:20px;white-space:nowrap;margin-right:0;grid-column:3;grid-row:1}.state-in_progress{background:#ebf3e5;color:#345b37}.state-waiting{background:#faf0d9;color:#735411}.state-planned{background:#ebe9f1;color:#5e576b}.state-deferred{background:#eeecea;color:#66616a}.stage-body{padding:0 48px 24px 64px;display:grid;grid-template-columns:1fr 1fr;gap:44px}.stage-body h4{font-size:12px;text-transform:uppercase;letter-spacing:1.1px;color:var(--purple);margin:17px 0 7px}.stage-body li,.stage-body p{font-size:15px;color:#57515f;line-height:1.6}.stage-body ul{padding-left:19px;margin:0}.stage-outcome{border-left:2px solid #dfdbeb;padding-left:22px}.stage-outcome p{margin:0 0 8px}
.compare{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:23px}.compare article{border:1px solid var(--line);border-radius:12px;background:white;padding:24px}.compare article:nth-child(3){border-color:#a59bd9;box-shadow:var(--shadow)}.compare small{color:var(--purple);font-weight:780;letter-spacing:1px;text-transform:uppercase;font-size:11px}.compare h3{font-size:20px;margin:9px 0}.compare p{font-size:15px;color:var(--muted);margin:0}.boundary-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:13px;margin-top:22px}.boundary{background:#fff;border:1px solid var(--line);border-radius:12px;padding:20px}.boundary strong{font-size:16px}.boundary p{font-size:14px;color:var(--muted);line-height:1.52;margin:8px 0 0}
.sources{list-style:none;padding:0;margin:22px 0;border-top:1px solid var(--line)}.sources li{display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid var(--line);padding:15px 5px}.sources li div{display:flex;gap:9px;flex-wrap:wrap;align-items:baseline}.sources li span{font-size:12px;color:var(--muted)}.sources a{font-weight:680}.external{color:var(--purple)!important}.glossary{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:20px}.glossary article{border-top:1px solid var(--line);padding-top:13px}.glossary dt{font-weight:740}.glossary dd{margin:5px 0;color:var(--muted);font-size:15px}.callout{border:1px solid #b6adf4;background:#f0eeff;border-radius:12px;padding:20px 24px;margin-top:20px}.callout h3{font-size:18px;margin:0 0 8px}.callout p{font-size:16px;margin:0}.end-panel{background:var(--deep);border-radius:17px;color:white;padding:33px;margin-top:37px}.end-panel h2{font-size:29px;color:#fff;margin:0 0 14px}.end-panel p{max-width:830px;color:#e0deea;font-size:19px}.end-panel small{color:#c8c3dc}footer{margin-top:65px;padding:24px 0;border-top:1px solid var(--line);color:var(--muted);font-size:13px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:20px}
.norm-groups{display:grid;grid-template-columns:1fr 1fr;gap:21px;margin-top:23px}.norm-group{background:white;border:1px solid var(--line);border-radius:14px;overflow:hidden}.norm-head{padding:24px 26px;background:#f0eefe;border-bottom:1px solid #dbd7ed}.norm-head h3{margin:9px 0;font-size:25px;letter-spacing:-.6px}.norm-head p{font-size:13px;color:var(--muted);margin:0 0 10px}.norm-head>a{font-size:14px}.norm-head .eyebrow{font-size:10px;letter-spacing:1px}.norm-item{border-bottom:1px solid var(--line)}.norm-item:last-child{border:0}.norm-item summary{padding:15px 22px;display:flex;align-items:center;justify-content:space-between;gap:10px;cursor:pointer;font-size:14px;line-height:1.5;list-style:none}.norm-item summary::-webkit-details-marker{display:none}.norm-item summary b{color:var(--purple);margin-right:7px}.norm-item[open] summary{background:#faf9fd}.norm-tag{flex-shrink:0;font-size:10px;color:#585168;border:1px solid #ddd8ec;border-radius:30px;padding:4px 7px}.norm-item-body{padding:1px 23px 20px;font-size:14px}.norm-item-body p{color:#484551;margin:12px 0}.norm-item-body code{white-space:normal;line-height:1.6;font-size:12px}.audit-panel{border:1px solid #ddd5bd;background:#fffdf6;border-radius:13px;padding:24px;margin-top:24px}.audit-panel h3{font-size:21px;margin:0 0 8px}.audit-panel p{font-size:15px;color:#56505c}.audit-facts{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:18px 0}.audit-facts div{background:white;border:1px solid #ebe3c7;padding:14px;border-radius:10px}.audit-facts strong{display:block;font-size:29px;line-height:1.1}.audit-facts span{font-size:12px;color:#56505c}.norm-method{border-left:2px solid #ada3d4;padding-left:20px;max-width:850px;margin-top:23px;font-size:16px;color:var(--muted)}
@media(max-width:1000px){.norm-groups{grid-template-columns:1fr}.metric-grid{grid-template-columns:repeat(2,1fr)}.hero{gap:30px}.navlinks{gap:12px}.hypotheses,.case-grid,.boundary-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:720px){.audit-facts{grid-template-columns:1fr}body{font-size:16px}.topbar{position:static}.nav{padding:17px 20px;align-items:flex-start;flex-direction:column}.navlinks{gap:14px}.navlinks a{font-size:12px}main{padding:0 20px 55px}.hero{display:block;padding:39px 0 27px}.hero h1{font-size:42px;letter-spacing:-1.9px}.hero p{font-size:19px}.hero-aside{margin-top:28px}.section{padding-top:52px}.metric-grid,.target-grid,.hypotheses,.flow-grid,.objects-grid,.case-grid,.compare,.boundary-grid,.glossary,.two-cols{grid-template-columns:1fr}.metric{min-height:0}.hypo-detail{grid-template-columns:1fr}.stage summary{grid-template-columns:43px 1fr;gap:12px}.state{grid-column:2;grid-row:2;justify-self:start;margin:0}.stage summary:after{grid-column:2;grid-row:1;justify-self:end}.stage-body{display:block;padding:0 10px 22px 55px}.stage-outcome{margin-top:16px}.section-head{display:block}.controls{margin-top:20px}.question-panel p{font-size:20px}.case{padding:18px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{body{background:#fff;font-size:11pt}main{max-width:none;padding:0 8px}.topbar,.hero-actions,.controls,.segment,footer{display:none}.hero{padding:20px 0}.hero h1{font-size:35pt}.section{padding-top:24px;break-inside:avoid}.metric-grid,.target-grid{grid-template-columns:repeat(4,1fr)}.metric,.hypothesis,.process-step,.case,.object{break-inside:avoid}.stage summary{padding:12px 0}.stage-body{display:block}.stage[open] .stage-body{display:block}.stage:not([open]) .stage-body{display:none}.question-panel,.end-panel{background:#fff!important;color:#111!important;border:1px solid #999}.question-panel p,.end-panel p{color:#222!important}a{color:#111}}
'''
JS = r'''
(() => {
 const audience = Array.from(document.querySelectorAll('[data-audience]'));
 const panels = Array.from(document.querySelectorAll('[data-panel]'));
 audience.forEach(btn => btn.addEventListener('click', () => {
   audience.forEach(x => x.setAttribute('aria-selected', String(x===btn)));
   panels.forEach(x => { x.hidden = x.dataset.panel!==btn.dataset.audience; });
 }));
 const stages=Array.from(document.querySelectorAll('.stage'));
 document.getElementById('expand-all')?.addEventListener('click',()=>stages.forEach(s=>s.open=true));
 document.getElementById('collapse-all')?.addEventListener('click',()=>stages.forEach(s=>s.open=false));
 document.getElementById('print-report')?.addEventListener('click',()=>window.print());
})();
'''

# Static content first. JavaScript is only a progressive-enhancement control.
content = STUDY
metrics=''.join(render_metric(m) for m in content['current'])
targets=''.join(f'<div class="target"><strong>{e(m["value"])}</strong><b>{e(m["label"])}</b><small>{e(m["note"])}</small></div>' for m in content['targets'])
reader_controls=''.join(f'<button type="button" role="tab" aria-selected="{str(i==0).lower()}" data-audience="{e(it["key"])}" aria-controls="panel-{e(it["key"])}">{e(it["title"])}</button>' for i,it in enumerate(content['audiences']))
reader_panels=''.join(f'<div class="audience-panel" role="tabpanel" id="panel-{e(it["key"])}" data-panel="{e(it["key"])}" {"hidden" if i else ""}><h3>{e(it["title"])}: what matters here</h3><p>{e(it["copy"])}</p></div>' for i,it in enumerate(content['audiences']))
hypotheses=''.join(render_hyp(it) for it in content['hypotheses'])
steps=''.join(render_step(it) for it in content['pipeline'])
objects=''.join(f'<article class="object"><small>{e(it["question"])}</small><h3>{e(it["name"])}</h3><p>{e(it["body"])}</p></article>' for it in content['objects'])
stages=''.join(render_stage(it) for it in content['stages'])
comparison=''.join(f'<article><small>{e(it["role"])}</small><h3>{e(it["name"])}</h3><p>{e(it["what"])}</p></article>' for it in content['comparison'])
boundaries=''.join(f'<div class="boundary"><strong>{e(it["title"])}</strong><p>{e(it["copy"])}</p></div>' for it in content['boundaries'])
sources=''.join(render_source(it) for it in content['source_links'])
glossary=''.join(f'<article><dt>{e(it["term"])}</dt><dd>{e(it["definition"])}</dd></article>' for it in content['glossary'])
case_fields=[('Context','setting'),('Possible risk','risk'),('Evidence needed','evidence'),('Normative interpretation','norm'),('Proposed control','control'),('Test / limits','test')]
case_cells=''.join(f'<div class="case-cell"><b>{e(k)}</b><p>{e(content["first_case"][v])}</p></div>' for k,v in case_fields)
normative_groups = render_source_groups()
audit_counts = {state:sum(x['classification']==state for x in SOURCE_AUDIT['tests']) for state in ('match','locator_mismatch','fetch_not_found')}


HTML=f'''<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="A source-traceable research protocol and visual roadmap for Catholic institutional AI risk and control evidence.">
<title>Node &amp; Norm · Catholic Institutional AI Risk Study · v{e(content['version'])}</title>
<style>{CSS}</style></head>
<body>
<header class="topbar"><nav class="nav" aria-label="Main navigation"><a class="brand" href="#top">node<span class="brand-dot">&amp;</span>norm</a>
<div class="navlinks"><a href="#position">Where we are</a><a href="#question">Research question</a><a href="#method">How the study works</a><a href="#catholic-sources">Catholic sources</a><a href="#roadmap">Roadmap</a><a href="#sources">Evidence &amp; sources</a></div></nav></header>
<main id="top">
<section class="hero" aria-labelledby="hero-title"><div><div class="eyebrow">Node &amp; Norm · Independent research · Working design</div><h1 id="hero-title">A clearer path from AI risk to evidence.</h1><p>{e(content['lead'])}</p>
<div class="hero-actions"><a class="button-link primary" href="#position">Begin the study</a><a class="button-link secondary" href="#roadmap">View the roadmap</a><a class="button-link secondary" href="https://github.com/node-and-norm/control-evidence-corpus/blob/research/catholic-institutional-ai-pilot/research/extensions/catholic-institutions/PROTOCOL.md" target="_blank" rel="noopener noreferrer">Read full protocol</a></div></div>
<aside class="hero-aside"><h2>What would justify confidence?</h2><p>{e(content['north_star'])}</p><small>Designed for researchers, engineers, theologians and Catholic institutional leaders.</small></aside></section>
<div class="strip"><span><b>{e(content['snapshot_label'])}</b></span><span>{e(content['status'])} · v{e(content['version'])}</span><span>Static, versioned report · no live data synchronization</span></div>
<section class="section" id="position"><div class="eyebrow">01 / Where the work stands</div><h2>We have a research design, not findings.</h2><p class="intro">This page is a guided study plan. It shows what Node &amp; Norm has decided to investigate, what evidence would answer the question, and what work still requires independent review.</p>
<div class="metric-grid">{metrics}</div><div class="hero-note"><p><strong>Evidence boundary:</strong> {e(content['warning'])}</p></div>
<h3 style="font-size:21px;margin:30px 0 4px">Provisional pilot coverage</h3><p class="small-note">Coverage targets help plan capacity. They do not establish representativeness, prevalence or validity.</p><div class="target-grid">{targets}</div></section>
<section class="section" id="readers"><div class="eyebrow">02 / How to read this study</div><h2>One study. Different questions from different readers.</h2><p class="intro">The explanation starts with an institutional decision and moves toward technical evidence. Select the perspective most relevant to your review.</p><div class="segment" role="tablist" aria-label="Reader perspective">{reader_controls}</div>{reader_panels}</section>
<section class="section" id="question"><div class="eyebrow">03 / Research question and contribution</div><h2>What does this method add?</h2><div class="two-cols"><div class="question-panel"><div class="eyebrow">Principal research question</div><p>{e(content['primary_question'])}</p></div><div class="contrast"><h3>Proposed contribution</h3><p>{e(content['contribution'])}</p><hr class="thin-rule"><h3>Competing explanation</h3><p>{e(content['alternative'])}</p></div></div>
<h3 style="font-size:24px;margin:34px 0 0">Hypotheses that can be challenged</h3><p class="small-note">H1 is a candidate primary hypothesis. All measures, comparison rules and thresholds require protocol freeze before confirmatory interpretation.</p><div class="hypotheses">{hypotheses}</div></section>
<section class="section" id="method"><div class="eyebrow">04 / Method in plain language</div><h2>The path from a source to a conclusion.</h2><p class="intro">The website map helps researchers find material. Screening, human review and controlled evaluations determine which stronger conclusions are warranted. Each stage has an independent evidentiary purpose.</p><div class="flow-grid">{steps}</div><p class="flow-caption">Planning diagram. Arrows indicate a proposed workflow, not an operating data feed or scientific finding.</p>
<h3 style="font-size:23px;margin:35px 0 10px">Five distinct research objects</h3><p class="small-note">These objects are connected through IDs and versions. They are never merged into an all-purpose risk score.</p><div class="objects-grid">{objects}</div>
<div class="case"><div class="case-header"><h3>{e(content['first_case']['title'])}</h3><span class="lozenge">Illustrative only</span></div><p class="small-note" style="margin-top:12px">{e(content['first_case']['disclaimer'])}</p><div class="case-grid">{case_cells}</div><div class="hero-note"><p><strong>What the example cannot establish:</strong> {e(content['first_case']['limit'])}</p></div></div></section>
<section class="section" id="catholic-sources"><div class="eyebrow">05 / Catholic sources and evidence questions</div><h2>Two Church documents. Eighteen questions to investigate.</h2><p class="intro">The first source register uses <em>Antiqua et Nova</em> (2025) and Pope Leo XIV's <em>Magnifica Humanitas</em> (2026). Both are important. Neither supplies a ready-made software-control checklist. The questions below are proposed by Node &amp; Norm and require qualified review.</p>
<div class="norm-groups">{normative_groups}</div>
<div class="norm-method"><p><strong>Research sequence:</strong> Locate the original paragraph → record a source concept → propose an institutional evidence question → identify relevant CEC observation dimensions → obtain independent qualified review → test technical controls separately.</p><p>The authoritative text is the Vatican publication. Magisterium AI is used for source discovery and triage, with exact paragraph verification before admission.</p></div>
<div class="audit-panel"><h3>Source retrieval integrity: a small verification check</h3><p>A six-interaction Magisterium MCP search/fetch check found that several retrieved <em>Magnifica Humanitas</em> paragraph locators did not align. These are technical observations about retrieval, <strong>not</strong> defects proven in the service or results of the Catholic pilot.</p><div class="audit-facts"><div><strong>{audit_counts['match']}</strong><span>Search/fetch matches</span></div><div><strong>{audit_counts['locator_mismatch']}</strong><span>Paragraph mismatches</span></div><div><strong>{audit_counts['fetch_not_found']}</strong><span>Fetch not found</span></div></div><p><strong>Admission rule:</strong> Compare the search URL, fetched reference, returned passage and original Vatican paragraph. Record disagreements without silent correction. No general reliability inference is justified by six interactions.</p></div></section>
<section class="section" id="roadmap"><div class="eyebrow">06 / Plan and evidence gates</div><div class="section-head"><div><h2>Research roadmap</h2><p class="intro">A phase is complete only when its specified evidence gate has been met. The current status is recorded manually in the versioned manifest.</p></div><div class="controls"><button id="expand-all" type="button">Expand all</button><button id="collapse-all" type="button">Collapse all</button><button id="print-report" type="button">Print / PDF</button></div></div><div class="stages">{stages}</div></section>
<section class="section" id="evaluation"><div class="eyebrow">07 / How the idea is tested</div><h2>Compare it with simpler methods.</h2><p class="intro">The study cannot assume that a detailed evidence record is automatically better. Three representations should be tested against the same source packets with a common support rubric and independent reviewers.</p><div class="compare">{comparison}</div><div class="callout"><h3>What would count against the research claim?</h3><p>A narrative or checklist may perform equally well with less burden. Reviewers may disagree about which controls were relevant. Public records may be too incomplete to support conclusions. Each result would be reportable, including a null or negative result.</p></div></section>
<section class="section" id="limits"><div class="eyebrow">08 / Scientific and institutional boundaries</div><h2>What we refuse to infer.</h2><div class="boundary-grid">{boundaries}</div><div class="callout"><h3>Church review is a distinct responsibility</h3><p>Technical annotations cannot settle doctrinal interpretation, canonical applicability, pastoral suitability or ecclesial authority. These judgments require source-located reasoning and appropriately qualified reviewers. Internal alignment with CDCF's C1–C8 criteria would remain a self-assessment until formally reviewed.</p></div></section>
<section class="section" id="sources"><div class="eyebrow">09 / Sources, terms and provenance</div><h2>Every substantive claim needs an inspectable source.</h2><p class="intro">These are source anchors for the design, not proof that the proposed study has been completed. Per-record source locators, rights and retrieved versions will be required at intake.</p><ul class="sources">{sources}</ul><h3 style="font-size:23px;margin:32px 0 0">Short glossary</h3><dl class="glossary">{glossary}</dl>
<h3 style="font-size:23px;margin:34px 0 0">Version history and updates</h3><p class="intro">This is a living, manually versioned research account. New sources, case decisions, protocol changes and corrections require dated entries. Prior versions must remain recoverable.</p><div class="case" style="margin-top:14px"><div class="case-header"><strong>v{e(content['version'])} · {e(content['date'])}</strong><span class="lozenge">Planning release</span></div><p style="margin:12px 0 0;font-size:15px">{e(content['changes'][0]['description'])}</p><p class="small-note" style="margin-top:8px">Source of record: study.json, PROTOCOL.md and DECISIONS.md on the dedicated CEC research branch.</p></div>
<div class="end-panel"><div class="eyebrow" style="color:#c3baff">Next consequential decision</div><h2>Freeze the method before selecting results.</h2><p>Complete the close-work literature comparison, assign qualified reviewers, decide the source frame and rights, and freeze the comparison protocol. Only then should the pilot be evaluated as evidence rather than treated as an illustration.</p><small>Version {e(content['version'])} · {e(content['date'])} · Node &amp; Norm research extension · No results claimed</small></div></section>
<footer><span>Node &amp; Norm · {e(content['id'])}</span><span>Living report: edit study.json + PROTOCOL.md, regenerate, review and record amendments.</span></footer>
</main><script>{JS}</script></body></html>'''

# --- Reproducible, human-readable Jupyter companion ---
# Notebook outputs are illustrations generated from the public planning manifest, never model or empirical outputs.

def md_cell(source): return {'cell_type':'markdown','metadata':{},'id': f'md-{hashlib.sha256(source.encode()).hexdigest()[:12]}','source': source.splitlines(keepends=True)}
def code_cell(source, outputs=None): return {'cell_type':'code','metadata':{},'id':f'code-{hashlib.sha256(source.encode()).hexdigest()[:12]}','execution_count':None,'source':source.splitlines(keepends=True),'outputs':outputs or []}
def md_table(headers, rows):
    def esc(x): return str(x).replace('|','\\|').replace('\n',' ')
    return '| ' + ' | '.join(map(esc,headers)) + ' |\n' + '| ' + ' | '.join(['---']*len(headers)) + ' |\n' + ''.join('| ' + ' | '.join(map(esc,row)) + ' |\n' for row in rows)

def architecture_svg():
    width, height = 1060, 260
    blocks=content['pipeline']
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d"><title id="t">Catholic research workflow</title><desc id="d">Six ordered stages: discover, screen, review, reconstruct, evaluate, report. Each requires separate review.</desc>','<rect x="0" y="0" width="1060" height="260" rx="18" fill="#f7f6f3"/>']
    for i, b in enumerate(blocks):
        x=28+i*174; w=150; y=53
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="132" rx="14" fill="#fff" stroke="#d7d1e7"/>')
        out.append(f'<text x="{x+16}" y="{y+25}" font-family="Arial,sans-serif" font-size="13" font-weight="bold" fill="#5145cd">{svg_escape(b["number"])}</text>')
        out.append(f'<text x="{x+16}" y="{y+62}" font-family="Arial,sans-serif" font-size="19" font-weight="bold" fill="#1c1923">{svg_escape(b["title"])}</text>')
        label=b['subtitle'].split(' and ')[0]
        if len(label)>19: label=label[:17]+'…'
        out.append(f'<text x="{x+16}" y="{y+87}" font-family="Arial,sans-serif" font-size="11" fill="#5f5b67">{svg_escape(label)}</text>')
        out.append(f'<text x="{x+16}" y="{y+113}" font-family="Arial,sans-serif" font-size="10" fill="#645d70">{svg_escape(b["status"][:23])}</text>')
        if i<5:
            out.append(f'<path d="M{x+w+3} {y+66} h15 m-6 -5 l6 5 -6 5" stroke="#5145cd" stroke-width="2" fill="none"/>')
    out.append('<text x="30" y="224" font-family="Arial,sans-serif" font-size="13" fill="#615a6a">Planning diagram only · no automatic data transfer or empirical result is represented</text></svg>')
    return ''.join(out)

svg=architecture_svg()
notebook_cells=[
 md_cell(f'''<div style="background:#1c1923;color:#fff;border-radius:16px;padding:27px 32px;">
<div style="letter-spacing:1.5px;color:#c6beff;font-size:13px;font-weight:bold;">NODE &amp; NORM · RESEARCH NOTEBOOK · v{content['version']}</div>
<h1 style="color:white;margin:13px 0 11px;">A clearer path from AI risk to evidence.</h1>
<p style="color:#e5e2f1;font-size:18px;">Catholic Institutional AI Risk and Control Evidence Pilot</p>
<p style="color:#c6bed4;font-size:14px;">{content['snapshot_label']} · Working research design · Not an empirical report</p>
</div>'''),
 md_cell('''## Start here: what this notebook can and cannot do\n\nThis is a **guided reader and reproducibility companion**. It explains the question, displays the proposed workflow, records the study's gates, and will later contain tested analyses. It does **not** connect automatically to the homepage, certify Catholic institutions, or supply human-reviewed findings.\n\nThe reader-first HTML report is `study-report.html`; the governing methodology is in `PROTOCOL.md`. All roadmap labels are drawn from `study.json`.'''),
 md_cell('## Current position\n\n'+md_table(['Measure','State','Meaning'],[(it['label'],it['value'],it['note']) for it in content['current']])+'\n**Pilot targets are planning ranges, not achieved sample sizes.**\n\n'+md_table(['Target','Count','Meaning'],[(it['label'],it['value'],it['note']) for it in content['targets']])),
 md_cell('## The research problem\n\n'+content['lead']+'\n\n> '+content['north_star']+'\n\n**Principal question**\n\n'+content['primary_question']+'\n\n**Contribution to test:** '+content['contribution']+'\n\n**Competing explanation:** '+content['alternative']),
 md_cell('## Hypotheses and failure conditions\n\n'+''.join(f'### {h["id"]} — {h["title"]} ({h["category"]})\n\n{h["claim"]}\n\n**Measure:** {h["measure"]}\n\n**Challenge:** {h["challenge"]}\n\n' for h in content['hypotheses'])),
 md_cell('## Visual workflow\n\nThe six stages below describe a planned research workflow. They should not be read as an operating automation.'),
 code_cell('''# A static planning diagram generated from study.json at build time.\n# Run this cell to re-display it. No external network or model calls.\nfrom IPython.display import display, SVG\nfrom pathlib import Path\n_svg = Path('assets/workflow.svg').read_text(encoding='utf-8')\ndisplay(SVG(_svg))\n''',outputs=[{'output_type':'display_data','data':{'image/svg+xml':svg},'metadata':{}}]),
 md_cell('## Distinguish the research objects\n\n'+md_table(['Object','Question','Evidentiary limit'],[(x['name'],x['question'],x['body']) for x in content['objects']])+'\n### Example: parish AI assistant\n\n*Hypothetical method example, not an actual case finding.*\n\n'+md_table(['Aspect','Illustration'],[(k.title(),content['first_case'][v]) for k,v in [('setting','setting'),('risk','risk'),('evidence','evidence'),('norm','norm'),('control','control'),('test','test')]])+'\n\n**Bound:** '+content['first_case']['limit']),
 md_cell('''## Catholic source layer: two documents, different questions

**Antiqua et Nova** (Dicasteries for the Doctrine of the Faith and for Culture and Education, 28 January 2025) addresses human dignity, moral responsibility, control, and institutional safeguards. [Official Vatican text](https://www.vatican.va/roman_curia/congregations/cfaith/documents/rc_ddf_doc_20250128_antiqua-et-nova_en.html).

**Magnifica Humanitas** (Leo XIV, signed 15 May 2026, publicly presented 25 May 2026) extends the discussion to the governance of AI, remedies, participatory oversight, institutional responsibility, and education. [Official Vatican text](https://www.vatican.va/content/leo-xiv/en/encyclicals/documents/20260515-magnifica-humanitas.html).

**Reading discipline:** A source paragraph is evidence of what the document teaches. A proposed technical-control question is a separate, reviewable hypothesis. Neither demonstrates operation or legal compliance.'''),
 md_cell('## Proposed source-to-CEC crosswalk (unreviewed)\n\n'+md_table(['Source','Theme','Candidate evidence question','CEC dimensions'], [(('Antiqua et Nova' if it['document_id']=='AN' else 'Magnifica Humanitas')+' §'+str(it['paragraph']),it['proposed_concept'],it['candidate_evidence_question'],', '.join(it['cec_dimensions'])) for it in CROSSWALK['records']])+'\n**All 18 rows are researcher-authored and require qualified independent theological or canonical review.** See `data/normative-crosswalk.json` for identifiers and source metadata.'),
 md_cell('## Magisterium connector source-fidelity check\n\nMagisterium AI can discover passages, but this small six-interaction check observed search/fetch locator disagreements for *Magnifica Humanitas*. The cause is unknown. This is not a measure of overall retrieval reliability.\n\n'+md_table(['Check','Document','Search paragraph','Fetched paragraph','Status'],[(t['id'],t['document'],t['search_expected_ref'],t['fetch_returned_ref'] or 'none',t['classification']) for t in SOURCE_AUDIT['tests']])+'\n**Rule:** a citation is admitted only after the retrieved locator is checked against the authoritative Vatican paragraph. Preserve mismatch and not-found results.'),
 code_cell('''# Structural checks only: verify the new source register and retrieval-log contracts.
# This cell does not query Magisterium or measure its accuracy.
from pathlib import Path
import json
r = Path.cwd()
crosswalk = json.loads((r/'data/normative-crosswalk.json').read_text())
audit = json.loads((r/'data/magisterium-locator-audit.json').read_text())
assert len(crosswalk['records']) == 18
assert {x['document_id'] for x in crosswalk['records']} == {'AN','MH'}
assert len({x['id'] for x in crosswalk['records']}) == len(crosswalk['records'])
assert len(audit['tests']) == 6
assert sum(x['classification']=='match' for x in audit['tests']) == 2
assert sum(x['classification']=='locator_mismatch' for x in audit['tests']) == 3
assert sum(x['classification']=='fetch_not_found' for x in audit['tests']) == 1
print('Source-register and locator-audit structure verified; independent normative review pending.')
'''),
 md_cell('## The comparative design\n\nThree evidence representations should receive the **same source content and retrieval cutoff**:\n\n'+md_table(['Method','Role','What reviewers see'],[(x['name'],x['role'],x['what']) for x in content['comparison']])+'\n\nInitial independent judgments must be retained, including disagreement and unresolved values. **No confirmatory result is authorized until the support rubric, assignment, precision target and acceptance thresholds are frozen.**'),
 md_cell('## The living roadmap\n\n'+md_table(['Phase','Stage','State','Evidence gate'],[(x['n'],x['name'],x['state'].replace('_',' '),x['gate']) for x in content['stages']])+'\nThe HTML version lets readers expand each stage to inspect specific outputs, dependencies and checks.'),
 md_cell('## The boundaries we protect\n\n'+''.join(f'- **{x["title"]}:** {x["copy"]}\n' for x in content['boundaries'])+'\nA Catholic doctrinal or canonical source does not automatically establish that a particular deployment violated Church teaching; qualified interpretation is separate.'),
 md_cell('## Source anchors\n\n'+''.join(f'- [{x["label"]}]({x["url"]}) — {x["kind"]}\n' for x in content['source_links'])+'\nFor empirical analysis, each record will need exact locators, source family, retrieval date, rights decision and version.'),
 md_cell('## Run basic reproducibility checks\n\nThe next cell verifies manifest metadata and the presence of the protocol. These are **document-integrity checks**, not scientific validation.'),
 code_cell('''from pathlib import Path\nimport json, hashlib\nroot = Path.cwd()\nstudy = json.loads((root / 'study.json').read_text(encoding='utf-8'))\nprotocol_bytes = (root / 'PROTOCOL.md').read_bytes()\nassert study['version'] == '0.2.0'\nassert len(study['stages']) == 7\nassert len(study['hypotheses']) == 4\nprint('Manifest version:', study['version'])\nprint('Planning phases:', len(study['stages']))\nprint('Protocol SHA-256:', hashlib.sha256(protocol_bytes).hexdigest())\nprint('Status:', study['status'])\nprint('No empirical research checks executed.')\n'''),
 md_cell('## Report, update and correction rule\n\nChanges to `study.json` update the roadmap and both reader artifacts after running `python scripts/build_study.py`. Changes to `PROTOCOL.md` require explicit review. Append substantive decisions to `DECISIONS.md`; retain versioned releases and preserve negative findings.\n\n**Next gate:** G0 — decide the source population, review roles, comparator metrics and preregistration rules before coding the main pilot.\n\n**Change history**\n\n'+md_table(['Date','Version','Change'],[(x['date'],x['version'],x['description']) for x in content['changes']]))
]
nb={
 'cells': notebook_cells,
 'metadata': {'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.11'},'title':'Catholic Institutional AI Risk and Control Evidence Pilot','node_and_norm':{'manifest_version':content['version'],'status':content['status'],'generated_from':'study.json + PROTOCOL.md','empirical_results':False}},
 'nbformat':4,'nbformat_minor':5
}
(ROOT/'assets').mkdir(exist_ok=True)
(ROOT/'assets/workflow.svg').write_text(svg,encoding='utf-8')
(ROOT/'study-report.html').write_text(HTML,encoding='utf-8')
(ROOT/'study-guide.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
print(f'Generated: {ROOT / "study-report.html"} ({len(HTML):,} chars)')
print(f'Generated: {ROOT / "study-guide.ipynb"} ({(ROOT / "study-guide.ipynb").stat().st_size:,} bytes)')
print(f'Generated: {ROOT / "assets/workflow.svg"}')
