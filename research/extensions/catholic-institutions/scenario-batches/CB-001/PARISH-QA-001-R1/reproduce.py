"""Offline checks for retained application-visible responses. No network or scoring."""
from pathlib import Path
from datetime import datetime
import hashlib,json
ROOT=Path(__file__).resolve().parent

def check(evidence:dict, draft:dict)->dict:
    rows=evidence['records']
    assert len(rows)==6
    assert [x['case_id'] for x in rows]==[x['id'] for x in draft['cases']]
    prefix=evidence['common_prefix']
    starts=[];references=[]
    for i,(row,case) in enumerate(zip(rows,draft['cases'])):
        assert row['prompt']==prefix+case['prompt']
        assert row['attempt']==1
        before=datetime.fromisoformat(row['recorded_before_call']);after=datetime.fromisoformat(row['recorded_after_call'])
        assert before<=after
        assert before>datetime.fromisoformat(evidence['plan_recorded_at'])
        starts.append(before)
        assert isinstance(row['response']['answer'],str) and row['response']['answer']
        assert isinstance(row['response']['references'],list)
        assert len(row['response']['answer'].split())<=250
        references.extend(row['response']['references'])
        assert row['canonical_review']=='pending_qualified_review'
        assert row['semantic_review']=='unadjudicated'
        assert row['correctness_score'] is None
        for ref in row['response']['references']:
            assert ref['source_url'].startswith('https://www.magisterium.com/docs/')
    gaps=[(b-a).total_seconds() for a,b in zip(starts,starts[1:])]
    assert min(gaps)>=31
    assert evidence['freeze_commit']=='62615b91434937c936f6828567cde75ce163627c'
    return {'kind':'record_integrity_check','cases':len(rows),'reference_entries':len(references),'unique_reference_urls':len({r['source_url'] for r in references}),'word_counts':[len(r['response']['answer'].split()) for r in rows],'minimum_local_start_gap_seconds':min(gaps),'qualified_correctness_established':False,'compliance_assessed':False,'network_calls':0}

if __name__=='__main__':
    e=json.loads((ROOT/'evidence.json').read_text())
    d=json.loads((ROOT.parent/'obligations/parish-test-plan.json').read_text())
    result=check(e,d)
    print(json.dumps(result,indent=2))
