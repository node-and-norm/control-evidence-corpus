"""Generate five draft reading files from the released base and frozen run.
No research requests. The run packet and TAE-aligned disclosure stay distinct.
"""
from pathlib import Path
import json,hashlib,html,re,copy
import mistune,nbformat
R=Path(__file__).parent
BASE=R.parent/'baseline'
OUT=R.parent/'rebuilt-readers'
OUT.mkdir(exist_ok=True)
render=mistune.create_markdown(escape=True,plugins=['table'])
load=lambda n:json.loads((R/n).read_text())
cases=load('cases.json');raw=load('raw-results.json');metrics=load('results.json');plan=load('plan.json');receipt=load('execution.json')
engine=(R/'engine.py').read_text()
assert hashlib.sha256(engine.encode()).hexdigest()==plan['input_sha256']['engine.py']
assert hashlib.sha256((R/'raw-results.json').read_bytes()).hexdigest()==receipt['raw_results_sha256']
# Reuse a single analysis/addendum text for HTML, protocol and notebook.
text='''## Pilot 02. Does more structure improve citation admission?

**CIR-001 · CITATION-GATE-001-R1 · Executed engineering feasibility comparison · Reading update 0.4.2-draft**

The simple checklist and structured gate made the same admission decisions. Both retained all eight constructed valid identities and held all sixteen invalid or unresolved cases. The structured gate showed no admission advantage here. Its more detailed trace may aid review, but that benefit has not been measured.

| Procedure | Valid identities retained | Positives on nonadmissible cases | Held / nonmatching | Meaning left unreviewed |
|---|---:|---:|---:|---:|
| Locator-only diagnostic (ablation) | 7 / 8 | 11 / 16 diagnostic signals | 6 / 24 | 24 / 24 |
| Simple checklist | 8 / 8 | 0 / 16 admissions | 16 / 24 | 24 / 24 |
| Structured gate | 8 / 8 | 0 / 16 admissions | 16 / 24 | 24 / 24 |

### What these numbers represent

There were 22 assistant-authored synthetic packets and two archived, previously known metadata failures. Three deterministic procedures generated 72 outputs in one pass. No new service query, LLM inference, human participant or institutional deployment was involved. The 72 outputs are not 72 independent cases.

All eight valid identities belong to the synthetic stratum. Its fourteen nonadmissible cases and the two known historical failures remain distinct. Both complete procedures apply the same criteria to the same evidence. Their agreement is an engineering conformance result, not a measurement-validity finding or proof of CEC superiority.

The locator-only arm is a diagnostic ablation adapted from the older archived-run field comparison. Its positive labels are not actual admission decisions by the website, Magisterium, or a Catholic institution.

### Follow two cases

**CG-10: the number matches, the document does not.** A constructed response retains paragraph44 but changes the document. The narrow diagnostic emits a match signal. Both complete procedures hold the record.

**CG-07: the identity matches, but meaning still needs review.** The synthetic input asserts that AI has approved its interpretation. Both complete procedures retain the identity while leaving semantic support unreviewed. An identity check has no authority to approve a theological answer.

### The source packet

Selected sections of NIST AI600-1 were inspected: section2.2, printed page6 / PDF page10, and actions MS-2.5-001 and MS-2.5-003, printed page31 / PDF page35. They motivate checking generated citations and limiting conclusions from narrow tests. Official English Antiqua et Nova44–46 and Magnifica Humanitas105–106 were inspected for provisional institutional context. This is targeted assistant inspection, not a full systematic review or qualified theological interpretation.

No original Vatican or NIST byte snapshot is claimed: direct original-byte downloads were unavailable. The packet uses source locators and bounded paraphrases. All bodies in the newly authored test fixtures are visibly invented. Neither a matching hash nor a passing test proves source truth.

### Freeze, results, and remaining work

The design and input/engine hashes were committed before execution at ec08b3efd74187fff948e22ebffbb623ecaa7015. The first run completed once without retries or tuning. Its raw outputs, first-run receipt, code and inputs are in the portable evidence package. Repository scripts recreate the fixed input bytes and produce replay copies that must match the first-run output digest. A replay is labelled as a replay, even when its bytes match.

The next step is a separately planned live-integration test and an independently prepared packet. Qualified review remains necessary for meaning and institutional applicability. Keep the checklist as the admission baseline; test any benefit of the richer trace rather than assuming it.

### AI disclosure for this increment

One ChatGPT assistant inspected selected sources, designed the packet, authored the code and reference expectations, executed the local comparison, and drafted these readers. Provider build details are unestablished. The same-assistant oracle limits independence. No multi-agent or independent human study occurred. Maintainer authorization is not personal source verification or exact-text approval. The existing TAE-aligned disclosure continues to apply, with this artifact-scoped contribution added.

**Scope:** one controlled identity-component comparison is now recorded. Zero independently reviewed Catholic safeguard studies, zero qualified normative approvals and zero canonical empirical admissions are established. The four other scenarios remain drafts. The published 0.4.1 release is preserved while this increment is reviewed in PR37.
'''
(R/'READER_ADDENDUM.md').write_text(text)
rows=['| Case | Construction / source | Reference | Diagnostic | Checklist / gate |','|---|---|---|---|---|']
for c in cases:
 o={x['procedure']:x['output'] for x in raw if x['case_id']==c['case_id']}
 rows.append(f"| {c['case_id']} | {c['label']} ({'synthetic' if c['origin']=='authored_synthetic' else 'historical replay'}) | {'identity-consistent' if c['reference_identity_admission'] else 'hold'} | {o['locator_diagnostic']['status']} | {o['simple_checklist']['status']} / {o['structured_gate']['status']} |")
table='\n'.join(rows)
extra_css='''\n.cir-result{margin:24px 0;background:#fff;border:1px solid var(--line);border-radius:14px;padding:28px;overflow-wrap:anywhere}.cir-result h2{font-size:29px}.cir-result h3{font-size:21px;margin-top:28px}.cir-result table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.5;margin:22px 0}.cir-result th,.cir-result td{border:1px solid var(--line);padding:11px;vertical-align:top;text-align:left}.cir-result th{background:var(--lav)}.cir-result summary{cursor:pointer;font-weight:650;padding:12px 0}.cir-scroll{overflow-x:auto}.cir-banner{background:var(--lav);border:1px solid var(--line);border-radius:12px;padding:18px 23px;margin:22px 0;font-size:16px;line-height:1.6}@media(max-width:760px){.cir-result{padding:18px}.cir-result table{min-width:600px}}@media print{.cir-result{padding:0;border:0;break-inside:auto}.cir-result table{font-size:8pt;table-layout:fixed;min-width:0!important}.cir-result td,.cir-result th{padding:6px;overflow-wrap:anywhere}.cir-scroll{overflow:visible}.cir-result h2,.cir-result h3{break-after:avoid}.cir-banner{padding:12px;font-size:10pt}.cir-result tr{break-inside:avoid}}\n'''
render_safe=lambda t:render(t).replace('<table>','<div class="cir-scroll"><table>').replace('</table>','</table></div>')
section='<section class="section" id="cir001-result"><div class="eyebrow">Current engineering evidence</div><div class="cir-result">'+render_safe(text)+'<details><summary>Inspect all 24 cases</summary>'+render_safe(table)+'</details></div></section>'
banner='<div class="cir-banner"><strong>Reading update 0.4.2-draft.</strong> The first citation-identity component comparison is recorded. The checklist and structured gate tied. This draft extends the preserved 0.4.1 study; it adds no independent or theological approval. <a href="#cir001-result">Read the result</a>.</div>'
base=(BASE/'study-report.html').read_text()
base=base.replace('</style>',extra_css+'</style>',1)
base=base.replace('<main>', '<main>'+banner,1)
base=base.replace('<section class="section" id="pilot-start">',section+'<section class="section" id="pilot-start">',1)
base=base.replace('<div class="navlinks">','<div class="navlinks"><a href="#cir001-result">CIR-001 result</a>',1)
base=base.replace('The first source run is recorded.','Source verification and one identity-component comparison are recorded.',1)
(OUT/'NodeNorm_Study_v0_4_2.html').write_text(base)
pmd=(BASE/'PROTOCOL.md').read_text()+'\n\n## Engineering addendum: CITATION-GATE-001-R1\n\nThe main comparative protocol remains 0.3.0 and unfrozen. This independently identified run freezes only its finite engineering conditions; no H1–H4 or human-review gate is waived.\n\n'+text+'\n\n### Fixed case inventory\n\n'+table+'\n'
(OUT/'NodeNorm_Protocol_v0_4_2.md').write_text(pmd)
ph=(BASE/'protocol.html').read_text().replace('</style>',extra_css+'</style>',1)
ph=ph.replace('</main>','<div class="cir-result">'+render_safe('## Engineering addendum: CITATION-GATE-001-R1\n\nCore protocol0.3.0 remains unfrozen.\n\n'+text)+'</div></main>',1)
(OUT/'NodeNorm_Protocol_v0_4_2.html').write_text(ph)
nb=nbformat.read(BASE/'study-guide.ipynb',as_version=4)
snapshot={'plan':plan,'receipt':receipt,'cases':cases,'registry':load('registry.json'),'raw_results':raw,'metrics':metrics,'source_packet':load('source-packet.json'),'engine':engine}
nb.cells.insert(1,nbformat.v4.new_markdown_cell(text+'\n\n### Case inventory\n\n'+table))
code="""# Offline replay; no external model or research requests.
import json, hashlib
CIR = json.loads("""+repr(json.dumps(snapshot,ensure_ascii=False))+""")
assert hashlib.sha256(CIR['engine'].encode()).hexdigest() == CIR['plan']['input_sha256']['engine.py']
ns = {'__name__': 'cir001_frozen_engine'}
exec(compile(CIR['engine'], 'CITATION-GATE-001 frozen engine', 'exec'), ns)
replica = []
for c in CIR['cases']:
    observed = {k:c[k] for k in ['target','selected','search_results','fetched','claim']}
    for name in ['locator_diagnostic','simple_checklist','structured_gate']:
        fn = ns[name]
        output = fn(observed) if name == 'locator_diagnostic' else fn(observed, CIR['registry'])
        replica.append({'case_id':c['case_id'],'origin':c['origin'],'procedure':name,'output':output})
assert replica == CIR['raw_results']
encoded = (json.dumps(replica, ensure_ascii=False, indent=2) + '\\n').encode()
assert hashlib.sha256(encoded).hexdigest() == CIR['receipt']['raw_results_sha256']
print('72 procedure outputs reproduced from 24 fixed cases.')
for name in ['simple_checklist','structured_gate']:
    d = CIR['metrics']['metrics'][name]['all']
    print(name, ': retained',d['retained_positive'],'/ 8; wrong admissions',d['positive_on_nonadmissible'],'/ 16')
print('No independent or theological approval. This execution is a replay, not new observations.')
"""
nb.cells.insert(2,nbformat.v4.new_code_cell(code))
nb.metadata['cir001_update']={'reading_version':'0.4.2-draft','run_id':receipt['run_id'],'baseline_reading':'0.4.1-dev','publication':'draft_PR37','independent_validation':False}
nbformat.write(nb,OUT/'NodeNorm_Notebook_v0_4_2.ipynb')
print('Four draft reader files built; PDF and execution checks next.')
