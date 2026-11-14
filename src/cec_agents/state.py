"""Workflow state and output contracts, separate from empirical CEC schemas."""
from typing import TypedDict
from .capabilities import TeamBlocked

class TeamState(TypedDict, total=False):
    packet_sha256: str
    results: dict[str, dict]
    status: str
    review_ack: dict
    draft: dict


def validate_result(role: str, result: dict, source_ids: set[str]) -> None:
    keys = {'agent_id','source_ids','finding','semantic_support','applicability','control_effectiveness','publication_status','disclosure'}
    if not isinstance(result, dict) or set(result) != keys or result['agent_id'] != role:
        raise TeamBlocked('Invalid role output contract.')
    if not isinstance(result['source_ids'], list) or not result['source_ids'] or not set(result['source_ids']) <= source_ids:
        raise TeamBlocked('Unknown or missing evidence links in output.')
    if not isinstance(result['finding'], str) or not result['finding']:
        raise TeamBlocked('Missing role finding.')
    for key, expected in [('semantic_support','unreviewed'),('applicability','pending_qualified_review'),
                          ('control_effectiveness','not_established'),('publication_status','review_only')]:
        if result[key] != expected:
            raise TeamBlocked('Role attempted to promote an unreviewed judgment: ' + key)
    d = result['disclosure']
    required = {'execution_kind','actual_model_calls','provider','model_id','model_id_reason','role','prompt_sha256','affected_artifact','human_checks','independent_reviewer'}
    if not isinstance(d, dict) or set(d) != required:
        raise TeamBlocked('Incomplete agent contribution disclosure.')
    if d['execution_kind'] != 'deterministic_fixture' or d['actual_model_calls'] != 0 or d['role'] != role:
        raise TeamBlocked('Fixture/model execution was misrepresented.')
    if d['human_checks'] != [] or d['independent_reviewer'] is not False or d['model_id'] is not None or not d['model_id_reason']:
        raise TeamBlocked('Invented model details or human review.')
    if not isinstance(d['prompt_sha256'], str) or len(d['prompt_sha256']) != 64:
        raise TeamBlocked('Prompt lineage missing.')

