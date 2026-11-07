"""Preserved AI-disclosure checks; no approval inferred."""
VERSION="0.1.0"
def validate_record(r):
    errors=[]
    if r.get('version') != VERSION: errors.append('unexpected_disclosure_version')
    if not r.get('statement') or not r.get('contributions'): errors.append('missing_statement_or_contributions')
    ids=[x.get('id') for x in r.get('tools',[])]
    if len(ids)!=len(set(ids)): errors.append('duplicate_tool_id')
    for t in r.get('tools',[]):
        if t.get('model_snapshot') is None and not t.get('unknown_reason'): errors.append('unknown_model_without_reason')
    for c in r.get('contributions',[]):
        if not c.get('artifact_scope') or not c.get('evidence_basis'): errors.append('contribution_without_scope_or_basis')
        if any(t not in ids for t in c.get('tools',[])): errors.append('unknown_tool_reference')
        if not c.get('human_review_status') or not c.get('independent_review_status'): errors.append('review_status_missing')
    p=r.get('publication',{})
    if p.get('ai_authors'): errors.append('ai_cannot_be_author')
    if p.get('target_venue') is None and p.get('venue_compliance')!='pending_venue_selection_and_recheck': errors.append('venue_compliance_without_venue')
    h=r.get('human_review',{})
    if h.get('authorization_is_source_verification') or h.get('authorization_is_release_approval_for_all_claims'): errors.append('authorization_overclaim')
    for group in ['specific_personal_review_attestations','independent_review_attestations','qualified_theological_review_attestations']:
        for a in h.get(group,[]):
            if not all(a.get(k) for k in ['reviewer','artifact_version','scope','review_date','limitations','ai_exposure']): errors.append('incomplete_human_attestation')
    for k in ['historical_prompt_reconstruction_permitted','public_secrets_permitted','public_sensitive_institutional_data_permitted','private_internal_reasoning_claimed']:
        if r.get('retention',{}).get(k) is not False: errors.append('unsafe_retention_claim:'+k)
    return sorted(set(errors))
