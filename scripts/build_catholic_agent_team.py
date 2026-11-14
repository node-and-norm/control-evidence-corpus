#!/usr/bin/env python3
"""Build one notebook from the spec and a genuinely executed offline graph fixture.
No external research calls. Original research data, root README and 40 archived
master notebook cells are protected by existing repository checks.
"""
from pathlib import Path
import contextlib, hashlib, importlib.metadata as meta, importlib.util
import io, json, os, platform, socket, subprocess, sys, tempfile, unittest
from unittest.mock import patch
import nbformat
ROOT=Path(__file__).resolve().parents[1]; B=ROOT/'catholic-ai-pilot'
J=lambda p:json.loads(p.read_text(encoding='utf-8'))
S=lambda c:''.join(c['source']) if isinstance(c['source'],list) else c['source']

def write(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def md(text):return nbformat.v4.new_markdown_cell(text)

def build():
 spec=J(B/'_evidence/agent-team/spec.json')
 historical=B/'_evidence/disclosure/historical-guidance-2026-10-27.json'
 hist_bytes=historical.read_bytes(); historical_sha=hashlib.sha256(hist_bytes).hexdigest()
 ver=meta.version('langgraph')
 if ver!='1.2.22':raise RuntimeError('Expected pinned LangGraph 1.2.22, found '+ver)
 modspec=importlib.util.spec_from_file_location('cec_agent_team',B/'_tools/agent_team.py')
 team=importlib.util.module_from_spec(modspec);modspec.loader.exec_module(team)
 with tempfile.TemporaryDirectory() as td:
  with patch.object(socket.socket,'connect',side_effect=AssertionError('Network disabled during fixture')),patch('socket.create_connection',side_effect=AssertionError('Network disabled during fixture')):
   result=team.run_demo(Path(td)/'run')
 result['environment']={'python':platform.python_version(),'platform':platform.platform(),
   'packages':{n:meta.version(n) for n in ['langgraph','langchain-core','langgraph-checkpoint','langsmith','nbformat']}}
 result['pre_generation_commit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 result['execution_time_utc']=team.trace.utc_now()
 result['spec_first_commit']='0205eef3b75739a67033bfc2411dd0f7bc66b610'
 result['developer_checks_independent']=False
 write(B/'_evidence/agent-team/engineering-run.json',result)
 policy={
  'record_id':'AGENT-TEAM-PUBLISHER-CHECK-20261114','checked_date':'2026-11-14',
  'historical_table':'catholic-ai-pilot/_evidence/disclosure/historical-guidance-2026-10-27.json',
  'historical_table_sha256':historical_sha,'historical_date_unchanged':True,
  'selected_venue':None,'venue_compliance':'pending_venue_selection_and_recheck',
  'verification_limit':'Assistant source inspection during engineering design, not independent legal/publisher compliance certification. Complete web tool transport logs were not exported.',
  'rows':[
   {'id':'DR-002','source':'ACM authorship policy','url':'https://www.acm.org/publications/policies/new-acm-policy-on-authorship','alternate_official_url':'https://prod-www.acm.bloomreach.cloud/publications/policies/new-acm-policy-on-authorship','access':'Canonical page returned 403; official indexed text accessed.','policy_update':'2026-05-14','application':'Substantive research uses belong in Methods; writing-only assistance is treated separately. Record design, sources, experiments, code, analysis and artifact contributions.'},
   {'id':'DR-003','source':'IEEE generated-content guidance','url':'https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/','access':'Official page read.','application':'Identify AI system, affected sections and extent in acknowledgments where required; grammar/editing has separate treatment.'},
   {'id':'DR-004','source':'Nature Portfolio AI policy','url':'https://www.nature.com/nature-portfolio/editorial-policies/ai','access':'Direct page redirected to blocked identity service; official indexed policy text accessed.','application':'Evaluative or interpretive use needs demonstrable human oversight, verification and disclosure. Human judgment and accountability cannot be delegated; protect confidential material.'},
   {'id':'DR-005','source':'Jan Christopher Cwik, Disclosure is not documentation','url':'https://link.springer.com/article/10.1186/s41073-026-00245-8','published':'2026-08-15','access':'Publisher article metadata and text inspected.','application':'Methodological example for richer documentation; NOT a compulsory publisher rule or universal standard.'},
   {'id':'DR-011','source':'No publication venue selected','url':None,'application':'Do not claim universal compliance. Review exact current venue requirements and manuscript placement before submission.'}
  ]}
 write(B/'_evidence/disclosure/agent-team-policy-check-20261114.json',policy)
 disclosure={'record_id':'AIU-AGENT-TEAM-20261114','date':'2026-11-14','assistant':'ChatGPT','exact_model_snapshot':None,
  'model_snapshot_reason':'Exact provider generation snapshot is not established in the retained development record.',
  'contributions':['Specification and acceptance criteria','Code and synthetic test authoring','Official policy and framework source inspection','Notebook synthesis and repository preparation'],
  'same_assistant_authored_code_and_tests':True,'live_model_calls':0,'live_mcp_calls':0,'actual_multi_model_study':False,
  'roles_executed':'Five deterministic Python fixtures orchestrated by LangGraph; role names do not establish independent AI experts.',
  'human_review_attestations':[],'independent_review':'pending','venue_compliance':'pending_venue_selection_and_recheck',
  'application_prompt_capture':'Spec prompts and resolved requests/results for the representative dry run are in engineering-run.json.',
  'development_capture_limit':'This ChatGPT development conversation and all external web/plugin outputs were not automatically intercepted by the new runner. Their complete verbatim transcript is not claimed.',
  'existing_evidence_unchanged':True,'publication_authorized':False,
  'remaining':['Reviewed live provider adapters','Durable isolated persistence','Authenticated approval and cancellation','Actual model adversarial evaluations','Source rights/privacy review','Issue #41 owner and expert decisions']}
 write(B/'_evidence/disclosure/agent-team-20261114.json',disclosure)
 roles='| Role | Bounded task |\n|---|---|\n'+'\n'.join('| **'+r['id'].replace('_',' ')+'** | '+r['purpose']+' |' for r in spec['roles'])
 controls='| Area | What this prototype supplies | What remains unestablished |\n|---|---|---|\n'+'\n'.join('| **'+x['area']+'** | '+x['prototype_control']+' | '+x['remaining']+' |' for x in spec['safety_assurance_map'])
 req='| Requirement | Acceptance test |\n|---|---|\n'+'\n'.join('| **'+r['id']+'** '+r['rule']+' | `'+r['test']+'` |' for r in spec['requirements'])
 policies='| Rule | How we apply it | Verification/access note |\n|---|---|---|\n'+'\n'.join('| **'+r['id']+'** '+r['source']+' | '+r['application']+' | '+r.get('access','Venue selection remains open.')+' |' for r in policy['rows'])
 cells=[
 md('![Node & Norm](assets/book-banner.svg)\n\n# 17. Spec-driven research agents, assurance and disclosure\n\n**Engineering prototype 0.1.0 | 14 November 2026 | No new empirical finding**\n\n[Contents](00_START_HERE.ipynb) · [Protocol](02_Research_Protocol.ipynb) · [AI disclosure](07_AI_Disclosure.ipynb) · [Exact trace requirements](16_Prompt_Output_Capture_Protocol.ipynb)\n\n**What runs:** a real LangGraph workflow with five deterministic synthetic role fixtures, a pause/resume boundary and exact visible traces. **What does not run:** live model agents, Magisterium retrieval, LegiScan ingestion, human expert review, publication or the confirmatory study. The original pilot observations remain unchanged.'),
 md('## Which framework are we using?\n\nThe **research framework is CEC and the pilot protocol**. The LangChain course informed scoping, bounded research, evidence retention and synthesis; that did not mean the previous pilot was already running LangGraph. This increment introduces a tested **LangGraph** orchestration prototype. LangChain model/tool integrations are future adapters. LangSmith is optional observability, not the source of record; cloud tracing is disabled here.\n\n[LangGraph official overview](https://docs.langchain.com/oss/python/langgraph/overview) distinguishes orchestration from LangChain integrations and LangSmith tracing. Graph nodes and checkpoints alone do not prove safety or sound reasoning.'),
 md('## Spec-driven engineering: before coding, specify what must remain true\n\nThe [versioned specification](_evidence/agent-team/spec.json) was committed at `0205eef` **before implementation**. It fixes roles, allowed capabilities, input/output states, disallowed claims, trace requirements and acceptance tests. The sequence is **specify → plan → implement → test against the spec → review → controlled release**.\n\n[Microsoft’s spec-first guidance](https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering/) motivates this approach. We are applying the method, not claiming installation or execution of GitHub Spec Kit. New requirements must produce an explicit spec revision and new tests; agents cannot rewrite their permissions.\n\nSoftware integration is separate from approving a research protocol or source interpretation. [Issue #41](https://github.com/node-and-norm/control-evidence-corpus/issues/41) remains the study-owner gate.'),
 md('## A bounded team, with accountable humans outside it\n\n'+roles+'\n\nA deterministic coordinator fixes the order and budget. A canon lawyer, theologian, privacy/technical reviewer and the research owner remain **human roles**, not AI personas. Several models agreeing would not establish independent peer review. The same assistant authored this prototype, its fixtures and its tests.'),
 md('## The workflow\n\n**Frozen synthetic packet → risk/incident links → source correspondence → obligation candidates → assurance critique → PAUSE → synthetic test acknowledgment → review-only synthesis.**\n\nThe pause uses LangGraph `interrupt()` and an in-memory checkpointer; the resumed node has no repeated role calls before the pause. The acknowledgment is explicitly a fixture token, never a human signature. [Official interrupt documentation](https://docs.langchain.com/oss/python/langgraph/interrupts) explains resumption semantics. Durable cross-process recovery, authenticated reviewers, revocation and live adapters remain unimplemented.\n\nThe research process remains **Discover → Screen → Review → Reconstruct → Evaluate → Report**. This prototype tests workflow plumbing, not completion of those scientific stages.'),
 md('## Where MIT, AI incidents, Magisterium and LegiScan belong\n\n| Input | Proper role | Boundary |\n|---|---|---|\n| MIT risk records | Candidate failure mechanisms and source IDs | A risk is not an observed institutional event |\n| Incident reports | Reported events or external analogues | A report is not proof of causation, harm or Catholic applicability |\n| Magisterium and original Church publications | Discover passages; verify original text and edition | Retrieval is not qualified interpretation or ecclesial approval |\n| Explorer and LegiScan | Legislative discovery, status, dates and governance context | An enacted or proposed bill is not automatically applicable to the case |\n| Institutional control evidence | Actions, opportunities, acknowledgments and effects | A written policy or referral suggestion is not proof an intervention worked |\n\nThis prototype reads **invented local records only**. It does not connect these services. The [Explorer](https://nodeandnorm.org/governance-map) explicitly distinguishes research relevance from legal applicability; its [LegiScan review record](https://nodeandnorm.org/assets/governance/legiscan-review.json) is a scoped published snapshot, not a fresh nationwide legal determination.'),
 md('## Does the Explorer cover safety, assurance, evaluation and governance?\n\n**It supports discovery and context. It does not replace the controls, tests, evidence or accountable decisions below.**\n\n'+controls+'\n\n[NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) organizes risk management around Govern, Map, Measure and Manage. This is an organizing crosswalk, not a certification or complete conformance assessment. We must evaluate both **the AI used to conduct our research** and **the institutional AI system being studied**.'),
 md('## AI disclosure is an acceptance criterion\n\n'+policies+'\n\nYour [27 October historical table](_evidence/disclosure/historical-guidance-2026-10-27.json) is unchanged. The [separate 14 November source check](_evidence/disclosure/agent-team-policy-check-20261114.json) preserves access limitations and avoids replacing the older review date. Current primary sources: [ACM indexed official policy](https://prod-www.acm.bloomreach.cloud/publications/policies/new-acm-policy-on-authorship), [IEEE](https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/), [Nature Portfolio](https://www.nature.com/nature-portfolio/editorial-policies/ai), and [Cwik](https://link.springer.com/article/10.1186/s41073-026-00245-8).\n\nThe team must disclose research design, source selection, code, interpretation and drafting assistance—not just grammar editing. A website statement never substitutes for the target manuscript’s disclosure.'),
 md('## Per-role contribution and trace record\n\nEach resolved role call records its exact prompt, supplied evidence, prior outputs, source/spec hashes, visible response and result-validation state through the existing recorder. Every role supplies its affected artifact, actual model/provider identity (or explicit non-applicability), human checks, and limits. **Missing disclosure or invented human approval blocks the result.**\n\nThe [complete representative fixture transcript](_evidence/agent-team/engineering-run.json) includes all five request/result pairs. The [engineering AI-use record](_evidence/disclosure/agent-team-20261114.json) distinguishes ChatGPT’s development contribution from the deterministic test roles. It does not claim a complete raw transcript of this ChatGPT conversation or hidden provider operations.'),
 md('## Acceptance criteria and tests\n\n'+req+'\n\nTests include denied live mode, forged source IDs, attempted self-approval, missing disclosure, stale packet hash, budget exhaustion, failed role output and pause/resume without duplicate role calls. A hostile instruction inside invented source text cannot create a capability: no external tools are bound. **That does not establish resistance of an actual LLM to every prompt-injection attack.**'),
 md('## Recorded engineering run\n\nThe real LangGraph runtime executed four deterministic roles, paused, then executed the fifth after a **synthetic** acknowledgment. The ten start/terminal trace events are preserved in the run record. There were **zero model calls, zero external research service calls and zero human review attestations**.\n\nThe following cell only reads the saved result. It does not run agents or make network calls.'),
 ]
 code="""from pathlib import Path
import json
ROOT = next((p for p in [Path.cwd(), *Path.cwd().parents] if (p/'catholic-ai-pilot').is_dir()), None)
if ROOT is None:
    raise FileNotFoundError('Open within a checked-out repository; no remote fallback is used.')
record = json.loads((ROOT/'catholic-ai-pilot/_evidence/agent-team/engineering-run.json').read_text())
assert record['live_model_calls'] == 0 and record['published'] is False
assert record['roles_before_pause'] == 4 and record['roles_after_resume'] == 5
assert record['trace_integrity']['successes'] == 5
print('LangGraph version:', record['environment']['packages']['langgraph'])
print('Fixture role calls:', record['roles_after_resume'])
print('Trace events:', len(record['events']))
print('Status:', record['final_status'])
print('Human review:', record['human_review'])
print('Live model calls:', record['live_model_calls'])
"""
 output=io.StringIO()
 with contextlib.redirect_stdout(output):exec(code,{'__name__':'__notebook__'})
 c=nbformat.v4.new_code_cell(code,execution_count=1,outputs=[nbformat.v4.new_output('stream',name='stdout',text=output.getvalue())]);cells.append(c)
 cells.append(md('## Run locally, without a provider key\n\nFrom the repository root in an isolated environment:\n\n```bash\npython -m pip install -r catholic-ai-pilot/_tools/agent-team-requirements.txt\nCEC_REQUIRE_AGENT_TEAM=1 python -m unittest discover -s tests -p test_catholic_agent_team.py -v\n```\n\nThe optional dependency is pinned at the top level; the engineering-run record contains the resolved versions used in CI. Installing packages requires network access; executing the fixture graph does not. This is not a fully hash-locked supply-chain audit. No paid provider key, Magisterium or LegiScan credential is needed. Never put credentials in notebooks or public logs.'))
 cells.append(md('## Before live agents or a research claim\n\nThe next steps are reviewed read-only source adapters; a named and versioned provider configuration; durable isolated checkpoints; authenticated, revocable human decisions; token/cost/time limits; redaction and incident response; source and output adversarial tests; and the existing issue #41 freeze. Preserve development/holdout separation and the fair uncertainty-aware checklist comparator.\n\nNo provider is connected by this change. No agent can modify the study, send a referral, publish a report, amend the approved scope or decide that the institution is compliant. A future engineering PR must demonstrate each capability before it is enabled.\n\n[Return to the study](../CATHOLIC_PILOT.ipynb) · [Owner review #41](https://github.com/node-and-norm/control-evidence-corpus/issues/41)'))
 nb=nbformat.v4.new_notebook(cells=cells,metadata={'kernelspec':{'name':'python3','language':'python','display_name':'Python 3'},'language_info':{'name':'python'},'node_norm':{'engineering_spec':'CEC-AGENT-TEAM-001','live_model_calls':0,'qualified_review':'pending','new_research_results':False}})
 nbformat.validate(nb);nbformat.write(nb,B/'17_Agent_Team_and_Assurance.ipynb')
 for rel,heading,link in [
  ('CATHOLIC_PILOT.ipynb','Spec-driven agent-team engineering','catholic-ai-pilot/17_Agent_Team_and_Assurance.ipynb'),
  ('catholic-ai-pilot/00_START_HERE.ipynb','Spec-driven agent-team engineering','17_Agent_Team_and_Assurance.ipynb'),
  ('catholic-ai-pilot/07_AI_Disclosure.ipynb','Agent-team disclosure and publication guidance','17_Agent_Team_and_Assurance.ipynb')]:
  p=ROOT/rel;n=J(p);marker='<!-- agent-team-001 -->'
  if marker not in S(n['cells'][0]):n['cells'][0]['source']=S(n['cells'][0])+f'\n\n{marker}\n**[{heading}]({link})** — offline LangGraph fixtures, not a live study; human and venue approvals remain pending.\n'
  write(p,n)
 toc=J(B/'myst.yml');manifest=J(B/'_provenance/book-manifest.json');name='17_Agent_Team_and_Assurance.ipynb'
 if not any(x['file']==name for x in toc['project']['toc']):toc['project']['toc'].append({'file':name,'title':'Spec-driven agent team, assurance and disclosure'})
 if not any(x['path']=='catholic-ai-pilot/'+name for x in manifest['chapters']):manifest['chapters'].append({'path':'catholic-ai-pilot/'+name,'title':'Spec-driven agent team, assurance and disclosure'})
 write(B/'myst.yml',toc);write(B/'_provenance/book-manifest.json',manifest)
 count=len(manifest['chapters'])+1
 for rel,old,new in [
  ('scripts/check_catholic_pilot.py','assert len(pages)==18 and len(set(pages))==18',f'assert len(pages)=={count} and len(set(pages))=={count}'),
  ('tests/test_catholic_pilot_integrity.py',"self.assertEqual(r['notebooks'],18)",f"self.assertEqual(r['notebooks'],{count})"),
  ('tests/test_catholic_pilot_integrity.py','self.assertEqual(len(toc),17)',f'self.assertEqual(len(toc),{count-1})')]:
  p=ROOT/rel;t=p.read_text()
  if old in t:p.write_text(t.replace(old,new))
  elif new not in t:raise RuntimeError('Unexpected notebook integrity guard: '+rel)
 index=ROOT/'catholic-ai-pilot/00_START_HERE.ipynb';n=J(index)
 for c in n['cells']:
  if '| Chapter | What you can inspect |' in S(c) and '[17. ' not in S(c):c['source']=S(c).rstrip()+'\n| [17. Agent team and assurance](17_Agent_Team_and_Assurance.ipynb) | Spec, deterministic LangGraph dry run, controls, disclosure and open live-study gates. |\n'
 write(index,n)
 if historical.read_bytes()!=hist_bytes:raise RuntimeError('Historical disclosure bytes changed')
 suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_catholic_agent_team.py')
 log=io.StringIO();out=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
 validation={'kind':'engineering_fixture_validation','tests_run':out.testsRun,'failures':len(out.failures),'errors':len(out.errors),'skipped':len(out.skipped),'success':out.wasSuccessful(),
   'requirement_ids':[r['id'] for r in spec['requirements']],'live_model_calls':0,'independent_validation':False,'log':log.getvalue(),
   'historical_disclosure_sha256':historical_sha,'spec_sha256':result['spec_sha256'],'input_packet_sha256':result['packet_sha256']}
 write(B/'_evidence/agent-team/validation.json',validation)
 print(log.getvalue());print(json.dumps({k:v for k,v in validation.items() if k!='log'},indent=2))
 if not out.wasSuccessful() or out.skipped:raise RuntimeError('Agent-team engineering tests failed or skipped')

if __name__=='__main__':build()
