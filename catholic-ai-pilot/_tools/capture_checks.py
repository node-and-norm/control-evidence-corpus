"""Preserved source-capture checks; no live requests."""
import json,hashlib
def derive(capture):
    records = capture['records']
    if len(records) != 4:
        raise ValueError('The bounded run must retain all four recorded calls.')
    plan_bytes = (json.dumps(capture['plan'], indent=2) + '\n').encode()
    if hashlib.sha256(plan_bytes).hexdigest() != capture['plan_sha256']:
        raise ValueError('Pre-call plan bytes do not match the retained hash.')
    rows = []
    for i, target in enumerate(capture['plan']['queries']):
        search, fetch = records[2*i:2*i+2]
        assert search['request']['query'] == target['query']
        chosen = next((r for r in search['response']['returned_items'] if r['id'] == fetch['request']['id']), None)
        if chosen is None:
            raise ValueError('Fetch identifier absent from the recorded search.')
        expected = chosen['url'].rstrip('/').split('/')[-1]
        actual = fetch['response'].get('metadata', {}).get('ref')
        outcome = 'fetch_not_found' if not fetch['response'].get('found') else ('locator_match' if actual == expected else 'locator_mismatch')
        rows.append({'target': target['target'], 'search_locator': expected, 'fetched_locator': actual, 'outcome': outcome})
    return rows
