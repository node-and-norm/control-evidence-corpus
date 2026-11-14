"""Engineering fixtures only. No model, live source, reviewer or institutional result.
Dedicated CI requires LangGraph; ordinary repository checks can inspect static contracts.
"""
from pathlib import Path
import copy, hashlib, importlib.util, json, os, socket, tempfile, unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'catholic-ai-pilot'
SPEC=BOOK/'_evidence/agent-team/spec.json'
HAS_LANGGRAPH=importlib.util.find_spec('langgraph') is not None
if os.getenv('CEC_REQUIRE_AGENT_TEAM')=='1' and not HAS_LANGGRAPH:
    raise RuntimeError('Dedicated agent-team validation requires its pinned LangGraph dependency.')
if HAS_LANGGRAPH:
    spec=importlib.util.spec_from_file_location('cec_agent_team',BOOK/'_tools/agent_team.py')
    team=importlib.util.module_from_spec(spec);spec.loader.exec_module(team)


class AgentTeamStatic(unittest.TestCase):
    def test_historical_disclosure_preserved(self):
        p=BOOK/'_evidence/disclosure/historical-guidance-2026-10-27.json'
        b=p.read_bytes();sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        self.assertEqual(sha,'db2b930890f7060c4357f94e569345c3b19074bc')
        r=json.loads(b);self.assertEqual(r['original_reference_date'],'2026-10-27')
        self.assertEqual({x['rule_id'] for x in r['rows']},{'DR-002','DR-003','DR-004','DR-005','DR-011'})

    def test_spec_requirement_traceability(self):
        s=json.loads(SPEC.read_text());self.assertFalse(s['live_execution_enabled'])
        self.assertFalse(s['publication_enabled']);self.assertFalse(s['research_freeze_authorized'])
        self.assertEqual(len(s['roles']),5)
        self.assertEqual(len({x['id'] for x in s['requirements']}),14)
        methods=set(dir(AgentTeamStatic))|set(dir(AgentTeamRuntime))
        self.assertTrue(all(x['test'] in methods for x in s['requirements']))

    def test_engineering_disclosure_scope(self):
        p=BOOK/'_evidence/disclosure/agent-team-20261114.json'
        if not p.exists():
            if os.getenv('CEC_REQUIRE_AGENT_TEAM')=='1':self.fail('Generated disclosure missing')
            self.skipTest('Reader generation not yet committed on preparation branch')
        d=json.loads(p.read_text())
        self.assertEqual(d['human_review_attestations'],[])
        self.assertEqual(d['live_model_calls'],0)
        self.assertTrue(d['same_assistant_authored_code_and_tests'])
        self.assertIsNone(d['exact_model_snapshot'])
        self.assertEqual(d['venue_compliance'],'pending_venue_selection_and_recheck')

    def test_workbook_has_no_network_or_secret_calls(self):
        p=BOOK/'17_Agent_Team_and_Assurance.ipynb'
        if not p.exists():
            if os.getenv('CEC_REQUIRE_AGENT_TEAM')=='1':self.fail('Generated notebook missing')
            self.skipTest('Reader generation not yet committed on preparation branch')
        n=json.loads(p.read_text());self.assertEqual(n['nbformat'],4)
        codes=[''.join(c['source']) if isinstance(c['source'],list) else c['source'] for c in n['cells'] if c['cell_type']=='code']
        self.assertEqual(len(codes),1)
        for bad in ['requests.','urlopen','api_key','subprocess.','run_demo(']:self.assertNotIn(bad,codes[0])
        self.assertEqual(n['metadata']['node_norm']['live_model_calls'],0)
        self.assertEqual(n['metadata']['node_norm']['qualified_review'],'pending')


@unittest.skipUnless(HAS_LANGGRAPH,'Install optional pinned agent-team dependencies for runtime tests')
class AgentTeamRuntime(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.run=Path(self.temp.name)/'run'
    def new(self,**kwargs):return team.OfflineAgentTeam(self.run,**kwargs)
    def test_live_mode_blocked(self):
        with self.assertRaises(team.TeamBlocked):self.new(mode='live')
        self.assertFalse(self.run.exists())
    def test_offline_graph_runs_without_network(self):
        with patch.object(socket.socket,'connect',side_effect=AssertionError('network denied')), patch('socket.create_connection',side_effect=AssertionError('network denied')):
            r=team.run_demo(self.run)
        self.assertEqual(r['live_model_calls'],0);self.assertTrue(r['pause_observed'])
        self.assertEqual(r['roles_before_pause'],4);self.assertEqual(r['roles_after_resume'],5)
        self.assertFalse(r['published']);self.assertEqual(r['trace_integrity']['successes'],5)
    def test_exact_prompts_and_outputs(self):
        t=self.new();t.start();t.resume_fixture();events=t.events()
        self.assertEqual(len(events),10)
        for role,request,response in zip(t.spec['roles'],events[::2],events[1::2]):
            self.assertEqual(request['prompt_text'],role['prompt'])
            self.assertEqual(request['visible_args']['prompt'],role['prompt'])
            self.assertEqual(response['response_text'],team.canonical(response['visible_result']).decode())
            self.assertEqual(request['prompt_sha256'],hashlib.sha256(role['prompt'].encode()).hexdigest())
            self.assertEqual(response['visible_result']['agent_id'],role['id'])
    def test_budget_blocks_before_next_call(self):
        t=self.new(max_calls=3)
        with self.assertRaises(team.trace.CaptureError):t.start()
        self.assertEqual(len(t.execution_order),3)
        self.assertEqual(team.trace.verify_run(t.run_dir)['unique_calls'],3)
    def test_source_instructions_cannot_expand_tools(self):
        t=self.new();t.start();r=t.resume_fixture()
        for name in ['shell.exec','github.merge','web.fetch','legiscan.write','send_email']:
            with self.assertRaises(team.TeamBlocked):t.authorize_tool(name)
        self.assertFalse(r['draft']['published'])
        self.assertIn('Ignore previous',t.lookup('SYN-CATHOLIC-01')['text'])
        with self.assertRaises(team.TeamBlocked):t.lookup('nonexistent-source')
    def test_forged_claim_and_approval_rejected(self):
        t=self.new();r=t._fixture_response(t.roles[0],{'prompt':'fixture'})
        for key,value in [('source_ids',['FAKE']),('applicability','compliant'),('semantic_support','verified'),('publication_status','published')]:
            bad=copy.deepcopy(r);bad[key]=value
            with self.assertRaises(team.TeamBlocked):t.validate_result(t.roles[0],bad)
    def test_pause_and_resume_without_repeating_roles(self):
        t=self.new();first=t.start()
        self.assertTrue(first['__interrupt__']);self.assertEqual(len(t.events()),8)
        t.resume_fixture();self.assertEqual(len(t.events()),10)
        self.assertEqual(len(set(t.execution_order)),5)
        with self.assertRaises(team.TeamBlocked):t.resume_fixture()
        with self.assertRaises(team.TeamBlocked):t.start()
        self.assertEqual(len(t.events()),10)
    def test_source_and_authority_states_remain_pending(self):
        t=self.new();t.start();r=t.resume_fixture()
        for row in r['results'].values():
            self.assertEqual(row['semantic_support'],'unreviewed')
            self.assertEqual(row['applicability'],'pending_qualified_review')
            self.assertEqual(row['control_effectiveness'],'not_established')
    def test_missing_disclosure_blocks_synthesis(self):
        t=self.new();r=t._fixture_response('synthesis_writer',{'prompt':'fixture'})
        r.pop('disclosure')
        with self.assertRaises(team.TeamBlocked):t.validate_result('synthesis_writer',r)
        r=t._fixture_response('synthesis_writer',{'prompt':'fixture'})
        r['disclosure']['human_checks']=['invented human approval']
        with self.assertRaises(team.TeamBlocked):t.validate_result('synthesis_writer',r)
    def test_fixture_ack_is_not_human_approval(self):
        t=self.new();t.start()
        with self.assertRaises(team.TeamBlocked):t.resume_fixture({'human_approved':True})
        r=t.resume_fixture();self.assertEqual(r['draft']['human_review'],'pending')
        with self.assertRaises(team.TeamBlocked):t.publication_decision()
    def test_explorer_is_not_assurance(self):
        t=self.new();t.start();r=t.resume_fixture()
        source=t.lookup('SYN-LAW-01');self.assertEqual(source['kind'],'legislative_candidate')
        row=r['results']['obligations_mapper']
        self.assertEqual(row['applicability'],'pending_qualified_review')
        self.assertEqual(row['control_effectiveness'],'not_established')
    def test_changed_packet_is_rejected(self):
        t=self.new();t.packet['question']='changed after preparation'
        with self.assertRaises(team.TeamBlocked):t.start()
        self.assertFalse((t.run_dir/'events.jsonl').exists())
    def test_private_and_duplicate_sources_are_rejected(self):
        p=team.synthetic_packet();p['real_people']=True
        with self.assertRaises(team.TeamBlocked):self.new(packet=p)
        p=team.synthetic_packet();p['sources'].append(copy.deepcopy(p['sources'][0]))
        with self.assertRaises(team.TeamBlocked):self.new(packet=p)
    def test_failure_is_captured_without_retry(self):
        t=self.new()
        def fail(*args):raise RuntimeError('synthetic failure')
        t._fixture_response=fail
        with self.assertRaises(RuntimeError):t.start()
        r=team.trace.verify_run(t.run_dir)
        self.assertEqual(r['errors'],1);self.assertEqual(r['unique_calls'],1)
    def test_role_cannot_write_into_repository(self):
        with self.assertRaises(team.TeamBlocked):team.OfflineAgentTeam(BOOK/'_evidence'/'forbidden-agent-write')
    def test_langsmith_cloud_disabled(self):
        self.assertEqual(os.environ['LANGSMITH_TRACING'],'false')
        self.assertEqual(os.environ['LANGCHAIN_TRACING_V2'],'false')

if __name__=='__main__':unittest.main()
