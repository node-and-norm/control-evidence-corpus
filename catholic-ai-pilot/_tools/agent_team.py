"""Compatibility entry point. Runtime implementation is in installed cec_agents.
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
