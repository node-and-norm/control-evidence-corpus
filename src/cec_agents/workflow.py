"""The single LangGraph coordinator; synthetic/offline behavior only."""
from __future__ import annotations
import copy,hashlib,json,os
from pathlib import Path
os.environ['LANGSMITH_TRACING']='false'
os.environ['LANGCHAIN_TRACING_V2']='false'
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, interrupt
from . import tracing as trace
from .contracts import canonical,digest
from .capabilities import TeamBlocked,require_offline,prepare_run_directory
from .roles import synthetic_packet,fixture_response
from .state import TeamState,validate_result
from .adapters import LocalPacketAdapter

class OfflineAgentTeam:
    """Sequential role graph with fixed capabilities and full visible fixture trace.

    Roles are future model-adapter slots. Runtime behavior here is deterministic
    software. A role label is not a model, expert or independent reviewer. The
    wrapper cannot stop arbitrary code outside this process.
    """
    def __init__(self, run_dir: Path, packet: dict | None = None, *, spec: dict, protected_root: Path, mode: str = 'offline_fixture', max_calls: int = 5):
        require_offline(mode, max_calls)
        self.spec = copy.deepcopy(spec)
        if self.spec['live_execution_enabled'] or self.spec['publication_enabled']:
            raise TeamBlocked('Prototype specification unexpectedly enables live activity or publication.')
        self.packet = copy.deepcopy(packet if packet is not None else synthetic_packet())
        if self.packet.get('kind') != 'synthetic_fixture' or self.packet.get('real_people') is not False:
            raise TeamBlocked('Only invented test records with no real people may enter this prototype.')
        if self.packet.get('source_rights') != 'invented_test_data':
            raise TeamBlocked('Prototype cannot process private, unreviewed or live source material.')
        sources = self.packet.get('sources')
        if not isinstance(sources, list) or not sources or not all(isinstance(s, dict) and isinstance(s.get('id'), str) for s in sources):
            raise TeamBlocked('Missing synthetic source records.')
        self.ids = {s['id'] for s in sources}
        if len(self.ids) != len(sources):
            raise TeamBlocked('Duplicate source IDs.')
        self.packet_hash = digest(self.packet)
        self.spec_hash = digest(self.spec)
        self.run_dir = prepare_run_directory(run_dir, protected_root)
        self.packet_adapter = LocalPacketAdapter(self.spec, self.packet, self.ids)
        self.run_id = 'SYNTHETIC-AGENT-TEAM-001'
        self.config = {'configurable': {'thread_id': self.run_id}, 'recursion_limit': 16}
        self.roles = [r['id'] for r in self.spec['roles']]
        if len(self.roles) != 5 or self.roles[-1] != 'synthesis_writer':
            raise TeamBlocked('Unexpected role specification.')
        plan = {'type': 'synthetic_engineering_fixture', 'spec_sha256': self.spec_hash, 'packet_sha256': self.packet_hash,
                'roles': self.roles, 'new_model_calls': 0, 'publication': False}
        plan_bytes = canonical(plan)
        (self.run_dir / 'plan.json').write_bytes(plan_bytes)
        manifest = {
            'schema': trace.VERSION, 'run_id': self.run_id, 'run_kind': 'offline_fixture',
            'fixture_disclosure': 'synthetic_unit_test_only_no_research_calls',
            'capture_scope': 'exact_caller_visible_payloads',
            'source_data_classification': 'synthetic_or_public_rights_cleared',
            'frozen_plan': {'relative_path': 'plan.json', 'sha256': hashlib.sha256(plan_bytes).hexdigest(), 'freeze_commit': None},
            'allowed_tools': [f'fixture.{r}' for r in self.roles], 'max_attempts': max_calls, 'approvals': {},
        }
        (self.run_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
        self._started = False
        self._paused = False
        self._finished = False
        self._fixture_ack = None
        self.execution_order: list[str] = []
        self._last = None
        self.graph = self._build()

    def authorize_tool(self, name: str) -> None:
        self.packet_adapter.authorize_tool(name)
    def lookup(self, source_id: str) -> dict:
        return self.packet_adapter.lookup(source_id)
    def _fixture_response(self, role: str, request: dict) -> dict:
        return fixture_response(role, request, self.ids)
    def validate_result(self, role: str, result: dict) -> None:
        validate_result(role, result, self.ids)
    def _call_role(self, role: str, state: TeamState) -> dict:
        if state['packet_sha256'] != self.packet_hash or digest(self.packet) != self.packet_hash or digest(self.spec) != self.spec_hash:
            raise TeamBlocked('Packet or spec changed after fixture preparation.')
        prompt = next(r['prompt'] for r in self.spec['roles'] if r['id'] == role)
        for previous, result in state.get('results', {}).items():
            self.validate_result(previous, result)
        request = {'prompt': prompt, 'packet': self.packet, 'prior_role_records': copy.deepcopy(state.get('results', {})),
                   'spec_sha256': self.spec_hash, 'packet_sha256': self.packet_hash, 'mode': 'synthetic_fixture_only'}
        output = trace.record_call(
            self.run_dir, call_id=f'{self.run_id}.{role}.1', case_id=role, attempt=1,
            kind='agent', tool_name=f'fixture.{role}', prompt_text=prompt, visible_args=request,
            provenance={'provider':'local.python.fixture','model_id':None,'model_id_state':'not_applicable',
                'model_id_unavailable_reason':'Deterministic fixture; no model exists.',
                'generation_parameters':None,'generation_parameters_state':'not_applicable',
                'parameters_unavailable_reason':'No generation model invoked.','transport_bytes_state':'not_captured'},
            invoke=lambda captured: self._fixture_response(role, captured),
            response_text_from=lambda visible: canonical(visible).decode('utf-8'), offline_fixture=True)
        self.validate_result(role, output)
        if output['disclosure']['prompt_sha256'] != hashlib.sha256(prompt.encode()).hexdigest():
            raise TeamBlocked('Disclosure prompt hash mismatch.')
        self.execution_order.append(role)
        return output

    def _build(self):
        g = StateGraph(TeamState)
        for role in self.roles[:-1]:
            def step(state, role=role):
                result = self._call_role(role, state)
                return {'results': {**state.get('results', {}), role: result}, 'status': 'working_fixture'}
            g.add_node(role, step)
        def review_pause(state):
            decision = interrupt({'kind':'fixture_review_boundary', 'run_id':self.run_id,
                'packet_sha256': self.packet_hash, 'original_packet':copy.deepcopy(self.packet),
                'human_review':'pending', 'analyst_labels_shown':False,
                'note':'Synthetic resume is a test action, never a human approval.'})
            expected = {'kind':'synthetic_fixture_ack','run_id':self.run_id,'packet_sha256':self.packet_hash,'continue':True}
            if decision != expected or self._fixture_ack != expected:
                raise TeamBlocked('Resume token is not bound to this synthetic test run.')
            return {'review_ack': decision, 'status':'fixture_acknowledged_not_human_approved'}
        def synthesize(state):
            if state.get('status') != 'fixture_acknowledged_not_human_approved':
                raise TeamBlocked('Required review-boundary interrupt was not traversed.')
            out = self._call_role('synthesis_writer', state)
            results = {**state['results'], 'synthesis_writer':out}
            if set(results) != set(self.roles):
                raise TeamBlocked('Missing role contributions.')
            for role, row in results.items(): self.validate_result(role, row)
            return {'results':results,'status':'draft_awaiting_qualified_review',
                'draft':{'kind':'synthetic_engineering_demo','roles':results,
                         'source_ids':sorted(self.ids),'human_review':'pending',
                         'venue_compliance':'pending_venue_selection','published':False,
                         'live_model_calls':0,'independent_validation':False}}
        g.add_node('review_pause', review_pause)
        g.add_node('synthesis_writer', synthesize)
        g.add_edge(START, self.roles[0])
        for first, second in zip(self.roles[:-2], self.roles[1:-1]): g.add_edge(first, second)
        g.add_edge(self.roles[-2], 'review_pause')
        g.add_edge('review_pause', 'synthesis_writer')
        g.add_edge('synthesis_writer', END)
        return g.compile(checkpointer=InMemorySaver())

    def start(self) -> dict:
        if self._started:
            raise TeamBlocked('Cannot restart and duplicate a retained trace. Resume the same run instead.')
        self._started = True
        result = self.graph.invoke({'packet_sha256':self.packet_hash,'results':{},'status':'ready_fixture'}, self.config)
        if not result.get('__interrupt__'):
            raise TeamBlocked('Required human-boundary interrupt did not occur.')
        self._paused = True
        self._last = result
        return result

    def resume_fixture(self, token: dict | None = None) -> dict:
        if not self._paused or self._finished:
            raise TeamBlocked('No paused fixture is available.')
        expected = {'kind':'synthetic_fixture_ack','run_id':self.run_id,'packet_sha256':self.packet_hash,'continue':True}
        if token is not None and token != expected:
            raise TeamBlocked('Invalid or misleading synthetic resume token.')
        self._fixture_ack = expected
        result = self.graph.invoke(Command(resume=expected), self.config)
        self._finished = True
        self._paused = False
        self._last = result
        trace.verify_run(self.run_dir)
        return result

    def publication_decision(self) -> None:
        raise TeamBlocked('Prototype cannot publish, certify or record qualified human approval.')

    def events(self) -> list[dict]:
        return [json.loads(line) for line in (self.run_dir/'events.jsonl').read_text(encoding='utf-8').splitlines()]


def run_demo(run_dir: Path, *, spec: dict, protected_root: Path) -> dict:
    """Run the actual LangGraph orchestration with zero LLM/API calls."""
    team = OfflineAgentTeam(run_dir, spec=spec, protected_root=protected_root)
    before = team.start()
    count_before = len(team.execution_order)
    final = team.resume_fixture()
    return {'kind':'synthetic_engineering_run_not_research','framework':'LangGraph',
            'spec_id':team.spec['spec_id'],'spec_sha256':team.spec_hash,'packet_sha256':team.packet_hash,
            'roles_before_pause':count_before,'roles_after_resume':len(team.execution_order),
            'order':team.execution_order,'pause_observed':bool(before.get('__interrupt__')),
            'final_status':final['status'],'human_review':'pending','published':False,'live_model_calls':0,
            'trace_integrity':trace.verify_run(team.run_dir),
            'events':team.events(),'draft':final['draft'],
            'limitations':['Deterministic fixtures, not model behavior or real sources.',
                'In-memory checkpoints only; no cross-process persistence or authenticated reviewers.',
                'Network isolation tested by denying socket access; no production security certification.',
                'Same assistant authored code, fixtures and tests; independent review pending.']}

