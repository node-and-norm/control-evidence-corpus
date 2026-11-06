"""Materialize frozen authored inputs; verify their hashes before any replay.

This is a portable form of the original fixture recipe. It is not a new sample,
a live retrieval, or independent labelling. Exact original input bytes are
checked against plan.json. The legacy public capture is an existing repository
input, not a newly invented provider response.
"""
from pathlib import Path
import argparse
import json
import hashlib
import copy

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--legacy', type=Path, required=True)
args = parser.parse_args()
R = args.output
R.mkdir(parents=True, exist_ok=True)
AN='429efa31-df0f-455d-b7e1-c104ed929e3b'
MH='ed397808-82f3-43e6-bf35-8f3f09fbdccc'
URL=lambda d,p:f'https://www.magisterium.com/docs/{d}/ref/{p}'
def dump(name,obj):
    p=R/name
    if p.exists(): raise FileExistsError('Do not overwrite retained inputs: '+str(p))
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def h(s):return hashlib.sha256(s.encode()).hexdigest()
registry={}
for d,p in [(AN,44),(AN,46),(MH,105),(MH,106)]:
    body=f'SYNTHETIC TEST CONTENT {d} paragraph {p}. Invented payload; no Church teaching is quoted.'
    registry[f'{d}:{p}:english-fixed:en']={'locator_observed':True,'normalized_sha256':h(body),'origin':'synthetic_reference_payload','body':body}
def base(d=AN,p=44):
    sid=f'fixture-{d[:4]}-{p}'
    body=registry[f'{d}:{p}:english-fixed:en']['body']
    s={'id':sid,'url':URL(d,p)}
    return {'target':{'document':d,'paragraph':p,'edition':'english-fixed','language':'en'},'selected':s,
    'search_results':[copy.deepcopy(s)],'fetched':{'requested_id':sid,'returned_id':sid,'found':True,'url':URL(d,p),'document':d,'ref':str(p),'edition':'english-fixed','language':'en','body':body},
    'claim':{'proposition':'Illustrative claim awaiting qualified source interpretation.','proposed_support':'unreviewed'}}
cases=[]
def add(label,case,expected,reason):
    cases.append({'case_id':f'CG-{len(cases)+1:02d}','label':label,'origin':'authored_synthetic',
    'reference_identity_admission':expected,'reference_semantic_support':'unreviewed','reference_reason':reason,**case})
for d,p in [(AN,44),(AN,46),(MH,105),(MH,106)]:add('Exact synthetic identity match',base(d,p),True,'All identity conditions satisfied for invented payload; no semantic approval.')
c=base();c['fetched']['ref']='para-44';add('Benign paragraph prefix',c,True,'Declared normalization allows para-44 and 44.')
c=base();c['fetched']['body']='\n  '+c['fetched']['body'].replace(' ','  ')+'\n';add('Benign whitespace',c,True,'Declared whitespace normalization preserves the invented payload.')
c=base(MH,105);c['claim']['proposed_support']='AI says fully supported';add('Model claims support',c,True,'Identity can match while model approval provides no qualified review.')
c=base(MH,106);c['claim']['proposition']='Does this source require our exact software control?';add('Normative inference unresolved',c,True,'Matching source cannot decide the proposed normative inference.')
c=base();c['fetched']['ref']='45';c['fetched']['url']=URL(AN,45);add('Wrong fetched paragraph',c,False,'Fetched paragraph differs from target.')
c=base();c['fetched']['document']=MH;c['fetched']['url']=URL(MH,44);add('Wrong document, same paragraph number',c,False,'Paragraph-number equality conceals a different document.')
c=base();c['fetched']={'requested_id':c['selected']['id'],'returned_id':c['selected']['id'],'found':False};add('Unavailable fetch',c,False,'No passage can be admitted.')
c=base();c['search_results'].append({'id':c['selected']['id'],'url':URL(AN,46)});add('Identifier bound to two paragraphs',c,False,'The chosen ID has conflicting bindings in the same retained response.')
c=base();c['fetched']['document']=MH;add('Document metadata conflicts with URL',c,False,'Contradictory document evidence is retained.')
c=base();c['fetched']['url']=URL(AN,46);add('URL conflicts with reference field',c,False,'A correct ref field cannot repair a different URL paragraph.')
c=base();c['fetched'].pop('ref');add('Paragraph metadata absent',c,False,'A missing check remains unresolved.')
c=base();c['target']['edition']='unregistered-edition';c['fetched']['edition']='unregistered-edition';add('No reference locator receipt',c,False,'Matching unregistered metadata lacks an inspected reference.')
c=base();c['fetched']['body']=None;add('Payload omitted',c,False,'No comparison can establish payload correspondence.')
c=base();c['fetched']['body']='SYNTHETIC altered body with copied citation fields.';add('Wrong payload, copied metadata',c,False,'Correct identity labels accompany a different invented payload.')
c=base();c['fetched']['edition']='different-edition';add('Wrong edition',c,False,'Edition differs from the frozen target.')
c=base();c['fetched']['language']='it';add('Wrong language',c,False,'Language differs from the frozen target.')
c=base();c['fetched']['url']='https://www.magisterium.com.example.invalid/docs/'+AN+'/ref/44';add('Lookalike source host',c,False,'A different hostname is outside the allowed pointer contract.')
c=base();c['fetched']['requested_id']='different-request';add('Request-response mismatch',c,False,'The fetched response is not bound to the selected request.')
cap=json.loads(args.legacy.read_text())
for i in range(2):
    sr,fr=cap['records'][2*i:2*i+2]
    se=next(x for x in sr['response']['returned_items'] if x['id']==fr['request']['id'])
    f=fr['response'];doc=AN if i==0 else MH;p=44 if i==0 else 105
    row={'case_id':f'CG-{len(cases)+1:02d}','label':'Archived source-run replay: '+cap['plan']['queries'][i]['target'],'origin':'historical_metadata_replay','reference_identity_admission':False,'reference_semantic_support':'unreviewed','reference_reason':'Known failure, deliberately retained as regression; no unseen sampling.',
    'target':{'document':doc,'paragraph':p,'edition':'english-fixed','language':'en'},'selected':{'id':se['id'],'url':se['url']},
    'search_results':[{'id':x['id'],'url':x['url']} for x in sr['response']['returned_items']],
    'fetched':{'requested_id':fr['request']['id'],'returned_id':f.get('id'),'found':f.get('found'),'url':f.get('url'),'ref':f.get('metadata',{}).get('ref'),'document':doc if f.get('found') else None,'edition':None,'language':None,'body':None},
    'claim':{'proposition':'No doctrinal proposition is evaluated by this replay.','proposed_support':'unreviewed'},
    'projection_limits':['Document field is derived from retained URL identity; edition, language and public body remain absent.','No new tool query or original provider byte capture occurred.'],
    'legacy_capture_sha256':hashlib.sha256(args.legacy.read_bytes()).hexdigest()}
    cases.append(row)
assert len(cases)==24 and sum(x['reference_identity_admission'] for x in cases)==8
dump('registry.json',registry);dump('cases.json',cases);dump('legacy-capture.json',cap)
plan=json.loads((Path(__file__).parent/'plan.json').read_text())
for name in ['registry.json','cases.json','legacy-capture.json']:
    actual=hashlib.sha256((R/name).read_bytes()).hexdigest()
    if actual != plan['input_sha256'][name]:raise ValueError('Frozen input correspondence failed: '+name)
print('Prepared 24 frozen cases; three generated input hashes match. No tested procedure invoked.')
