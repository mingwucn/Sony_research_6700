"""Invented metadata/cache bytes only; no cached Python is compiled/executed."""
import base64
import copy
import json
import unittest
from tools import dependency_legacy_comparison as c


def fixture():
    old={n:dict(role=n) for n in c.HISTORICAL}
    roles={'r'+str(i):{} for i in range(26)}
    old['role_authority']=dict(roles=roles)
    config=dict(operation_id='1'*32,source_rows={'alias'+str(i):{} for i in range(11)},
        trusted_origins={'trusted'+str(i):dict(path='C:/runtime/t'+str(i)+'.py') for i in range(4)})
    old['dependency_config']=config
    keys={'role:'+n for n in roles}|{'bootstrap:'+n for n in ('activation_gate','activation_binding','io_entry')}
    keys|={'integration:'+n for n in ('runtime_entry','gdt_wiring','prospective_child')}
    keys|={'dependency:'+n for n in config['source_rows']}|{'trusted:'+n for n in config['trusted_origins']}
    texts={n:('raise RuntimeError("invented must never execute '+n+'")\n').encode() for n in keys}
    rows={n:dict(path='C:/invented/source'+str(i)+'.py',**c.receipt(b),base64=base64.b64encode(b).decode()) for i,(n,b) in enumerate(sorted(texts.items()))}
    old['source_cache']=dict(schema='ordinary_python_source_cache_v1',sources=rows)
    old['source_manifest']=dict(bytes=1024017848,sha256='a'*64)
    old['prerequisites']=dict(constants_sha256='b'*64)
    historical={n:c.encoded(v) for n,v in old.items()}
    sources={'bound.'+n:b for n,b in texts.items() if n.startswith('role:') or n in ('bootstrap:activation_binding','bootstrap:io_entry','integration:prospective_child')}
    ordinary={n:historical[n] if n in c.RETAINED else c.encoded(dict(role=n)) for n in c.ORDINARY}
    ordinary['activity_rights']=c.encoded(dict(schema='gdt_observation_activity_dispositions_v1',operation_id='2'*32,camera_commands=[],scope_sha256=c.sha(ordinary['activity_scope']),decisions={n:dict(disposition='pending',evidence=[]) for n in c.DECISIONS}))
    request=c.encoded(dict(schema='gdt_observation_request_core_v1',operation_id='2'*32))
    proposal=c.encoded(dict(schema='gdt_observation_proposal_v1',operation_id='2'*32,camera_commands=[],request_sha256=c.sha(request),ordinary={n:c.receipt(b) for n,b in ordinary.items()},protected_identities=dict(firmware_package=old['source_manifest'],operational_constants=dict(bytes=123,sha256='b'*64))))
    args=dict(historical_buffers=historical,ordinary_buffers=ordinary,retained_source_buffers=sources,
        request_bytes=request,expected_request_sha256=c.sha(request),proposal_bytes=proposal,expected_proposal_sha256=c.sha(proposal))
    return refresh_map(args)


def refresh_map(a):
    references={n:dict(path='private/sessions/invented/'+n+'.json',**c.receipt(b)) for n,b in a['historical_buffers'].items()}
    profile=c.sha(c.encoded({k:v for k,v in json.loads(a['historical_buffers']['dependency_config']).items() if k!='operation_id'}))
    mapping=dict(references=references,reference_pins={n:references[n]['sha256'] for n in c.FIXED}|dict(dependency_profile=profile),dependency_profile_sha256=profile,raw_fixed_references=22,ordinary_input_documents=25,execution_authorized=False,camera_commands=[])
    a['reference_map_bytes']=c.encoded(mapping);a['expected_reference_map_sha256']=c.sha(a['reference_map_bytes']);return a


def change(a,role,fn):
    v=json.loads(a['historical_buffers'][role]);fn(v);a['historical_buffers'][role]=c.encoded(v)


class LegacyComparisonTests(unittest.TestCase):
    def setUp(self):self.a=fixture()

    def test_distinct_contexts_preserve_bytes_and_never_authorize(self):
        before=copy.deepcopy(self.a);r=c.compare(**self.a);self.assertEqual(self.a,before)
        self.assertTrue(r['operation_ids_differ']);self.assertEqual(r['compared_inputs'],25)
        self.assertEqual(r['retained_source_copies'],29);self.assertEqual(r['compared_cache_sources'],47)
        for key in ('execution_authorized','historical_authority_promoted','operational_path_qualified',
                    'full_legacy_gate_semantics_validated','full_proposal_semantics_validated',
                    'feature_supported','recovery_proven','device_write_gate_passed'):
            self.assertIs(r[key],False)

    def test_each_selected_anchor_is_external_to_local_resealing(self):
        for key in ('reference_map','proposal','request'):
            a=copy.deepcopy(self.a);a['expected_'+key+'_sha256']='f'*64
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'selected_anchor'):c.compare(**a)

    def test_all_historical_paths_and_bytes_are_bound(self):
        for role in c.HISTORICAL:
            a=copy.deepcopy(self.a);a['historical_buffers'][role]+=b' '
            with self.subTest(role=role),self.assertRaisesRegex(ValueError,'original_bytes'):c.compare(**a)

    def test_map_cannot_claim_authority(self):
        v=json.loads(self.a['reference_map_bytes']);v['execution_authorized']=True
        self.a['reference_map_bytes']=c.encoded(v);self.a['expected_reference_map_sha256']=c.sha(self.a['reference_map_bytes'])
        with self.assertRaisesRegex(ValueError,'map_mode'):c.compare(**self.a)

    def test_fixed_pin_survives_rehashed_reference_row(self):
        a=self.a;a['historical_buffers']['q_old_result']+=b' '
        v=json.loads(a['reference_map_bytes']);v['references']['q_old_result'].update(c.receipt(a['historical_buffers']['q_old_result']))
        a['reference_map_bytes']=c.encoded(v);a['expected_reference_map_sha256']=c.sha(a['reference_map_bytes'])
        with self.assertRaisesRegex(ValueError,'fixed_reference'):c.compare(**a)

    def test_each_of_six_originals_is_retained_after_map_reseal(self):
        for role in c.RETAINED:
            a=copy.deepcopy(self.a);a['historical_buffers'][role]+=b' ';refresh_map(a)
            with self.subTest(role=role),self.assertRaisesRegex(ValueError,'retained_bytes'):c.compare(**a)

    def test_profile_change_refuses_even_with_matching_input_row(self):
        change(self.a,'dependency_config',lambda v:v.update(extra='changed'))
        v=json.loads(self.a['reference_map_bytes']);v['references']['dependency_config'].update(c.receipt(self.a['historical_buffers']['dependency_config']))
        self.a['reference_map_bytes']=c.encoded(v);self.a['expected_reference_map_sha256']=c.sha(self.a['reference_map_bytes'])
        with self.assertRaisesRegex(ValueError,'dependency_profile'):c.compare(**self.a)

    def test_cache_tamper_is_detected_after_metadata_reseal(self):
        for field,value in (('base64',base64.b64encode(b'changed').decode()),('bytes',True),('sha256','c'*64),('base64','!bad')):
            a=copy.deepcopy(self.a);change(a,'source_cache',lambda v:v['sources']['role:r0'].update({field:value}));refresh_map(a)
            with self.subTest(field=field),self.assertRaises(ValueError):c.compare(**a)

    def test_path_alias_traversal_and_relative_cache_paths_refuse(self):
        for path in ('relative.py','C:/invented/../outside.py','C:/invented/x.dll'):
            a=copy.deepcopy(self.a);change(a,'source_cache',lambda v:v['sources']['role:r0'].update(path=path));refresh_map(a)
            with self.subTest(path=path),self.assertRaisesRegex(ValueError,'source_path'):c.compare(**a)
        rows=json.loads(self.a['historical_buffers']['source_cache'])['sources'];other=rows['role:r1']['path'].replace('/','\\')
        change(self.a,'source_cache',lambda v:v['sources']['role:r0'].update(path=other));refresh_map(self.a)
        with self.assertRaisesRegex(ValueError,'source_path'):c.compare(**self.a)

    def test_roster_omissions_and_extras_refuse(self):
        for group in ('historical_buffers','ordinary_buffers','retained_source_buffers'):
            for mode in ('missing','extra'):
                a=copy.deepcopy(self.a)
                if mode=='missing':a[group].pop(next(iter(a[group])))
                else:a[group]['extra']=b'{}'
                with self.subTest(group=group,mode=mode),self.assertRaises(ValueError):c.compare(**a)

    def test_retained_source_bytes_cannot_be_replaced(self):
        self.a['retained_source_buffers']['bound.role:r0']=b'changed'
        with self.assertRaisesRegex(ValueError,'retained_source'):c.compare(**self.a)

    def test_pending_decisions_cannot_be_promoted_or_relabelled(self):
        for status in ('allow_scope','deny_scope'):
            a=copy.deepcopy(self.a);v=json.loads(a['ordinary_buffers']['activity_rights']);v['decisions'][next(iter(c.DECISIONS))]['disposition']=status
            a['ordinary_buffers']['activity_rights']=c.encoded(v);p=json.loads(a['proposal_bytes']);p['ordinary']={n:c.receipt(b) for n,b in a['ordinary_buffers'].items()}
            a['proposal_bytes']=c.encoded(p);a['expected_proposal_sha256']=c.sha(a['proposal_bytes'])
            with self.subTest(status=status),self.assertRaisesRegex(ValueError,'pending_only'):c.compare(**a)

    def test_protected_identity_change_does_not_read_any_payload(self):
        p=json.loads(self.a['proposal_bytes']);p['protected_identities']['firmware_package']['sha256']='c'*64
        self.a['proposal_bytes']=c.encoded(p);self.a['expected_proposal_sha256']=c.sha(self.a['proposal_bytes'])
        with self.assertRaisesRegex(ValueError,'protected_metadata'):c.compare(**self.a)

    def test_duplicate_nonfinite_deep_and_nonbytes_json_refuse(self):
        for raw in (b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":1e999}',b'['*40+b'0'+b']'*40,b'\xff',bytearray(b'{}')):
            with self.subTest(raw=raw[:20]),self.assertRaises(ValueError):c.decode(raw)

    def test_invalid_map_path_and_boolean_count_refuse(self):
        for mutate in (lambda v:v.update(ordinary_input_documents=True),lambda v:v['references']['basis'].update(path='private/sessions/../bad.json')):
            a=copy.deepcopy(self.a);v=json.loads(a['reference_map_bytes']);mutate(v)
            a['reference_map_bytes']=c.encoded(v);a['expected_reference_map_sha256']=c.sha(a['reference_map_bytes'])
            with self.assertRaises(ValueError):c.compare(**a)

    def test_data_comparison_does_not_execute_or_open(self):
        from unittest.mock import patch
        with patch('builtins.open',side_effect=AssertionError('no file I/O')),patch('builtins.compile',side_effect=AssertionError('no source execution')):
            self.assertFalse(c.compare(**self.a)['execution_authorized'])
