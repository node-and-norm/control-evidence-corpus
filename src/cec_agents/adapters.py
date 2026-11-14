"""Only read-only local packet access is implemented. No remote adapters."""
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
