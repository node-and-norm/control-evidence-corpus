#!/usr/bin/env python3
"""One-time, hash-guarded architecture migration. No research/service calls.
The migration is executed on the engineering branch only, then retired.
"""
from pathlib import Path
import ast, hashlib, json, shutil, textwrap
ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'catholic-ai-pilot'
BASE='ab5140f9b80d84380186496c0d89c7f6323de5b6'
SHA=lambda b:hashlib.sha256(b).hexdigest()
def write(path,text):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def dump(path,obj):write(path,json.dumps(obj,indent=1,ensure_ascii=False)+'\n')
def text(c):return ''.join(c['source']) if isinstance(c['source'],list) else c['source']
def md(i,s):return {'cell_type':'markdown','id':i,'metadata':{'node_norm':{'kind':'architecture_maintenance','research_result':False}},'source':s}
plan=json.loads((ROOT/'specs/agent-team/runtime-layout.json').read_text())
for path,sha in plan['baseline_modules'].items():
 if SHA((ROOT/path).read_bytes())!=sha:raise RuntimeError('Changed baseline: '+path)
if SHA((ROOT/plan['frozen_behavior_spec']['path']).read_bytes())!=plan['frozen_behavior_spec']['file_sha256']:raise RuntimeError('Spec drift')
protected={p.relative_to(ROOT).as_posix():SHA(p.read_bytes()) for p in BOOK.rglob('*') if p.is_file() and ('_evidence' in p.parts or '_provenance' in p.parts)}
for path in ['README.md','CATHOLIC_PILOT.ipynb']:
 protected[path]=SHA((ROOT/path).read_bytes())
old=(BOOK/'_tools/agent_team.py').read_text(); lines=old.splitlines(keepends=True); tree=ast.parse(old)
def segment(node):return ''.join(lines[node.lineno-1:node.end_lineno])
nodes={x.name:x for x in tree.body if isinstance(x,(ast.ClassDef,ast.FunctionDef))}
cls=nodes['OfflineAgentTeam'];methods={x.name:x for x in cls.body if isinstance(x,ast.FunctionDef)}
def method(name):return segment(methods[name])
def transformed_function(name,signature,replacements=()):
 s=textwrap.dedent(method(name));s=s.replace(s.splitlines()[0],signature,1)
 for a,b in replacements:s=s.replace(a,b)
 return s+'\n'
write('src/cec_agents/__init__.py','''"""CEC research runtime: no provider adapters, no automatic execution."""
__version__ = '0.1.0.dev1'
''')
write('src/cec_agents/contracts.py','''"""Explicit input identity and serialization; no repository-global state."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from typing import Any
from .capabilities import TeamBlocked

'''+segment(nodes['canonical'])+'\n\n'+segment(nodes['digest'])+'''

def load_spec(path: Path, expected_sha256: str) -> dict:
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected_sha256:
        raise TeamBlocked('Specification bytes differ from the approved layout manifest.')
    value=json.loads(raw)
    if not isinstance(value,dict):
        raise TeamBlocked('Specification must be a JSON object.')
    return value
''')
write('src/cec_agents/capabilities.py','''"""Deterministic permission guards. Not an operating-system sandbox."""
from pathlib import Path

'''+segment(nodes['TeamBlocked'])+'''

def require_offline(mode: str, max_calls: int) -> None:
    if mode != 'offline_fixture':
        raise TeamBlocked('Live mode is disabled. Issue #41 and reviewed provider adapters are required.')
    if isinstance(max_calls, bool) or not isinstance(max_calls, int) or not 1 <= max_calls <= 5:
        raise TeamBlocked('Prototype permits one to five explicitly recorded role calls.')

def prepare_run_directory(run_dir: Path, protected_root: Path) -> Path:
    target=Path(run_dir).resolve(); protected=Path(protected_root).resolve()
    if target==protected or protected in target.parents:
        raise TeamBlocked('Use a temporary directory outside the repository; role execution cannot modify the corpus.')
    target.mkdir(parents=True,exist_ok=True)
    if any(target.iterdir()):
        raise TeamBlocked('A new run needs an empty directory; retained attempts must not be overwritten.')
    return target
''')
role=transformed_function('_fixture_response','def fixture_response(role: str, request: dict, source_ids: set[str]) -> dict:', [('self.ids','source_ids')])
write('src/cec_agents/roles.py','''"""Synthetic role outputs only. These functions are not LLMs or experts."""
import hashlib

'''+segment(nodes['synthetic_packet'])+'\n\n'+role)
valid=transformed_function('validate_result','def validate_result(role: str, result: dict, source_ids: set[str]) -> None:', [('self.ids','source_ids')])
write('src/cec_agents/state.py','''"""Workflow state and output contracts, separate from empirical CEC schemas."""
from typing import TypedDict
from .capabilities import TeamBlocked

'''+segment(nodes['TeamState'])+'\n\n'+valid)
write('src/cec_agents/adapters.py','''"""Only read-only local packet access is implemented. No remote adapters."""
import copy
from .capabilities import TeamBlocked

class LocalPacketAdapter:
    def __init__(self,spec: dict,packet: dict,source_ids: set[str]):
        self.spec=spec;self.packet=packet;self.source_ids=source_ids
    def authorize_tool(self,name: str) -> None:
        if name != self.spec['capabilities']['permitted_fixture_tool']:
            raise TeamBlocked('Capability denied: '+name)
    def lookup(self,source_id: str) -> dict:
        self.authorize_tool('packet.lookup')
        if source_id not in self.source_ids:
            raise TeamBlocked('Unknown evidence identifier.')
        return copy.deepcopy(next(s for s in self.packet['sources'] if s['id']==source_id))
''')
p=ROOT/'src/cec_agents/tracing.py';p.parent.mkdir(parents=True,exist_ok=True)
p.write_bytes((BOOK/'_tools/prompt_trace.py').read_bytes())
workflow=segment(cls)
old_init=method('__init__');new_init=old_init
new_init=new_init.replace("*, mode: str = 'offline_fixture', max_calls: int = 5)","*, spec: dict, protected_root: Path, mode: str = 'offline_fixture', max_calls: int = 5)")
start=new_init.index("        if mode != 'offline_fixture':")
end=new_init.index("        if self.spec['live_execution_enabled']")
new_init=new_init[:start]+"        require_offline(mode, max_calls)\n        self.spec = copy.deepcopy(spec)\n"+new_init[end:]
start=new_init.index('        self.run_dir = Path(run_dir).resolve()')
end=new_init.index("        self.run_id = 'SYNTHETIC-AGENT-TEAM-001'")
new_init=new_init[:start]+"        self.run_dir = prepare_run_directory(run_dir, protected_root)\n        self.packet_adapter = LocalPacketAdapter(self.spec, self.packet, self.ids)\n"+new_init[end:]
workflow=workflow.replace(old_init,new_init)
for name,replacement in {
 'authorize_tool':"    def authorize_tool(self, name: str) -> None:\n        self.packet_adapter.authorize_tool(name)",
 'lookup':"    def lookup(self, source_id: str) -> dict:\n        return self.packet_adapter.lookup(source_id)",
 '_fixture_response':"    def _fixture_response(self, role: str, request: dict) -> dict:\n        return fixture_response(role, request, self.ids)",
 'validate_result':"    def validate_result(self, role: str, result: dict) -> None:\n        validate_result(role, result, self.ids)"
}.items():workflow=workflow.replace(method(name),replacement)
demo=segment(nodes['run_demo']).replace('def run_demo(run_dir: Path) -> dict:', 'def run_demo(run_dir: Path, *, spec: dict, protected_root: Path) -> dict:').replace('team = OfflineAgentTeam(run_dir)','team = OfflineAgentTeam(run_dir, spec=spec, protected_root=protected_root)')
write('src/cec_agents/workflow.py','''"""The single LangGraph coordinator; synthetic/offline behavior only."""
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

'''+workflow+'\n\n'+demo+'\n')
write('catholic-ai-pilot/_tools/agent_team.py','''"""Compatibility entry point. Runtime implementation is in installed cec_agents.
Run from a checkout after: python -m pip install '.[agents]'
No prompts or research evidence are duplicated into the package.
"""
from pathlib import Path
import json
from cec_agents import tracing as trace
from cec_agents.contracts import canonical,digest,load_spec as _load_spec
from cec_agents.capabilities import TeamBlocked
from cec_agents.roles import synthetic_packet
from cec_agents.workflow import OfflineAgentTeam as _Team,run_demo as _demo
ROOT=Path(__file__).resolve().parents[2]
BOOK=ROOT/'catholic-ai-pilot'
_LAYOUT=ROOT/'specs/agent-team/runtime-layout.json'

def load_spec():
    entry=json.loads(_LAYOUT.read_text(encoding='utf-8'))['frozen_behavior_spec']
    return _load_spec(ROOT/entry['path'],entry['file_sha256'])

class OfflineAgentTeam(_Team):
    def __init__(self,run_dir,packet=None,*,mode='offline_fixture',max_calls=5):
        super().__init__(run_dir,packet,spec=load_spec(),protected_root=ROOT,mode=mode,max_calls=max_calls)

def run_demo(run_dir):
    return _demo(run_dir,spec=load_spec(),protected_root=ROOT)
''')
write('catholic-ai-pilot/_tools/prompt_trace.py','''#!/usr/bin/env python3
"""Historical import/CLI path forwarding to the single installed trace module."""
from cec_agents.tracing import (VERSION, APPROVALS, KNOWN_KIND, CaptureError,
    canonical,sha256_bytes,utc_now,validate_manifest,verify_events,verify_run,
    promotion_gate,record_call,main)
if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (CaptureError,OSError,ValueError) as exc:
        print('CAPTURE GATE BLOCKED:',str(exc))
        raise SystemExit(2)
''')
write('pyproject.toml','''[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "cec-research-agents"
version = "0.1.0.dev1"
description = "Offline research-agent engineering for Control Evidence Corpus; no live provider adapters"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
agents = ["langgraph==1.2.22"]

[tool.setuptools.packages.find]
where = ["src"]
include = ["cec_agents*"]
namespaces = false

[tool.setuptools]
include-package-data = false
''')
write('catholic-ai-pilot/_tools/agent-team-requirements.txt',"# Compatibility install entry. Invoke from repository root.\n# pyproject.toml is the authoritative package/dependency declaration.\n.[agents]\n")
write('scripts/build_catholic_agent_team.py','''#!/usr/bin/env python3
"""Compatibility command: validate the existing prototype; never regenerate evidence.
The original builder remains at baseline commit ab5140f9 for historical reproduction.
"""
from check_catholic_agent_package import main
if __name__=='__main__':
    raise SystemExit(main())
''')
ignore=(ROOT/'.gitignore').read_text()
for line in ['dist/','*.egg-info/']:
 if line not in ignore.splitlines():ignore+=line+'\n'
write('.gitignore',ignore)
p=BOOK/'17_Agent_Team_and_Assurance.ipynb';n=json.loads(p.read_text())
architecture='''## Repository architecture: one study, one runtime, one evidence record

**Architecture refactor, 14 November 2026.** The root workbook and existing chapter URLs remain unchanged. This is an engineering change, not a new empirical result.

| Responsibility | Authoritative location | Boundary |
|---|---|---|
| Study and human reading | Root `CATHOLIC_PILOT.ipynb` and the numbered notebooks | No code installation is needed to read saved results |
| Routing and pause/resume | [src/cec_agents/workflow.py](../src/cec_agents/workflow.py) | One coordinator; in-memory checkpoints only |
| Synthetic role behaviors | [roles.py](../src/cec_agents/roles.py) | Deterministic fixtures, not AI experts |
| State and output contracts | [state.py](../src/cec_agents/state.py) | Separate from the existing empirical CEC schemas |
| Permissions and output guards | [capabilities.py](../src/cec_agents/capabilities.py) | Process checks, not an operating-system sandbox |
| Source access | [adapters.py](../src/cec_agents/adapters.py) | Local read-only packet lookup; no remote providers |
| Exact visible trace | [tracing.py](../src/cec_agents/tracing.py) | Original implementation moved byte-for-byte |
| Active layout and provenance | [specs/agent-team/runtime-layout.json](../specs/agent-team/runtime-layout.json) | Points to the single preserved behavior specification and checks its hash |
| Research evidence | Existing `_evidence` records | Existing records are unchanged; no duplicate archive |

The original helper paths remain as small forwarding entry points, so old notebooks and commands continue to resolve. The runtime has no implicit dependency on the notebook folder: installed callers supply the specification and the protected repository root explicitly. Credentials, live-service adapters, a public API and autonomous publication remain absent.

**Supply-chain boundary:** LangGraph retains the previously tested top-level pin; CI records resolved dependency versions. This is not a fully hash-locked environment or independent supply-chain audit.

[Architecture acceptance specification](../specs/agent-team/runtime-layout.json) · [AI-use and migration limitations](_provenance/runtime-refactor.json)
'''
n['cells'].insert(3,md('runtime-architecture-20261114',architecture))
for c in n['cells']:
 if text(c).startswith('## Run locally, without a provider key'):
  c['source']='''## Run locally, without a provider key

Reading this notebook needs no installation. For optional engineering checks, create a virtual environment and run from the repository root:

```bash
python -m pip install '.[agents]' -r requirements.txt -r catholic-ai-pilot/requirements.txt
CEC_REQUIRE_AGENT_TEAM=1 python -m unittest discover -s tests -p 'test_catholic_agent*.py' -v
python scripts/check_catholic_agent_package.py
```

Installing dependencies requires package-network access. Fixture execution is tested with network calls denied and performs no live model or research-service requests. The package is also built as a wheel and exercised from a directory outside the checkout in CI; that distinguishes an installed package from accidental source-directory imports. The optional recorder retains its original Unix file-lock dependency. Windows support is unvalidated.

The old builder command now validates without rewriting retained evidence. Historical source reproduction remains available at its pinned Git commit.
'''
dump('catholic-ai-pilot/17_Agent_Team_and_Assurance.ipynb',n)
p=BOOK/'09_Reproduce_and_Inspect.ipynb';n=json.loads(p.read_text())
n['cells'].append(md('package-reproduction-20261114','''## Installed runtime and behavior-preserving refactor

The [architecture section in Chapter 17](17_Agent_Team_and_Assurance.ipynb) maps each runtime responsibility. Existing notebook URLs, frozen evidence and the root workbook remain unchanged.

From the repository root, install `.[agents]` before running optional helper commands. All old helper paths forward to the installed `cec_agents` package; only one implementation is maintained. The active layout record points to the original versioned role prompts instead of copying them into the wheel.

```bash
python -m pip install '.[agents]' -r requirements.txt -r catholic-ai-pilot/requirements.txt
python scripts/check_catholic_agent_package.py
```

The new checker compares the complete deterministic inputs/outputs, role sequence, pause/resume and retained failure behavior with the baseline implementation at commit `ab5140f9b80d84380186496c0d89c7f6323de5b6`. Only recorded UTC timestamps, the chain hashes derived from those timestamps, and absolute temporary run paths are normalized. No prompt, response, source identifier, result field, budget or authority status is ignored.

The acceptance workflow separately builds a wheel, installs it, changes outside the checkout, clears `PYTHONPATH`, and repeats the comparison. It retains a machine report as a CI artifact. A passed software comparison does not constitute canonical, theological or scientific approval. [Scope and disclosure record](_provenance/runtime-refactor.json).
'''))
dump('catholic-ai-pilot/09_Reproduce_and_Inspect.ipynb',n)
record={
 'record_id':'CEC-RUNTIME-REFACTOR-20261114','baseline_commit':BASE,'specification_commit':'90c6c7c2eaf4f926d16569865a6e6bd13b064ef4',
 'scope':'Behavior-preserving package extraction; no live connections or new research results',
 'protected_file_sha256':protected,
 'trace_module_moved_byte_identically':{'from':'catholic-ai-pilot/_tools/prompt_trace.py','to':'src/cec_agents/tracing.py','sha256':plan['baseline_modules']['catholic-ai-pilot/_tools/prompt_trace.py']},
 'canonical_runtime':'src/cec_agents','compatibility_wrappers':['catholic-ai-pilot/_tools/agent_team.py','catholic-ai-pilot/_tools/prompt_trace.py'],
 'retired_builder':'Original writing builder remains available at the baseline commit; current command is validation-only.',
 'normalization_scope':['recorded_at_utc in events only','previous_sha256 and event_sha256 linked to those timestamps','trace_integrity.last_sha256','trace_integrity.run_dir'],
 'validation_status':'Pending execution; CI artifacts are authoritative, this record is not a test-success assertion.',
 'ai_use':{'assistant':'ChatGPT','exact_model_snapshot':None,'roles':['architecture specification','AST-assisted extraction','test authoring','notebook maintenance','repository integration'],'same_assistant_authored_code_and_tests':True,'human_review_attestations':[],'live_model_calls':0,'live_research_service_calls':0,'development_capture_limit':'This maintenance conversation is not an automatically captured provider transport log.'},
 'known_limitations':['Only deterministic fixtures; no LLM behavior finding','In-memory checkpoint; no authenticated or durable approval','Process-level path/capability guards; not an OS sandbox','Top-level dependency pin; transitive resolutions recorded in CI, not fully hash locked','Existing trace implementation limitations preserved for behavioral equivalence','Source evidence and original disclosures remain exactly as recorded'],
 'issue_41_completed':False,'publication_enabled':False,'independent_validation':False}
dump('catholic-ai-pilot/_provenance/runtime-refactor.json',record)
for path,expected in protected.items():
 if SHA((ROOT/path).read_bytes())!=expected:raise RuntimeError('Protected bytes changed: '+path)
for p in (ROOT/'src/cec_agents').glob('*.py'):compile(p.read_text(),str(p),'exec')
print(json.dumps({'generated_runtime_modules':8,'protected_files':len(protected),'new_research_calls':0,'root_notebook_unchanged':True},indent=2))
