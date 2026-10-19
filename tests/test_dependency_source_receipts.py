"""Invented source buffers and metadata; no file or dependency activation."""
import copy
import stat
import unittest
from unittest.mock import patch

from tools import dependency_source_receipts as subject
from tests.test_dependency_basis_links import fixture as basis_fixture
from tests.test_dependency_input_semantics import fixture as dependency_fixture
from tests.test_dependency_authority_grammar import chain, raw


def add_source_records(candidate,args,dependency_anchor):
    pre=subject.envelope.decode(args['ordinary_buffers']['prerequisites'])
    sources={};rows={}
    for index,role in enumerate(sorted(subject.envelope.SOURCE_ROLES)):
        value=args['source_buffers'][role]
        path=(pre['qualified_roles'][role.split(':',1)[1]]['path'] if role.startswith('bound.role:')
              else 'private/invented-support/source_%02d.py'%index)
        stamp=dict(device=7,inode=index+1,mode=stat.S_IFREG|0o600,nlink=1,size=len(value),
            mtime_ns=1234,ctime_ns=5678,file_attributes=0)
        sources[role]=dict(path=path,bytes=len(value),sha256=subject.envelope.sha(value),
            identity={k:stamp[k] for k in subject.evidence.CROSS})
        receipt=dict(path='D:/invented-root/'+path,size=len(value),sha256=subject.envelope.sha(value),
            opened_read_only=True,**{k:dict(stamp) for k in ('lstat_before','fstat_before','fstat_after','lstat_after')})
        rows[role]=dict(receipt=receipt,close_attempts=1,eof_probes=1,read_calls=2,closed=True)
    manifest=dict(schema='invented_authored_source_manifest_v1',invented=True,
        operation_id=dependency_anchor['operation_id'],root_path='D:/invented-root',sources=sources,camera_commands=[])
    args['ordinary_buffers']['authored_source_manifest']=raw(manifest)
    receipts=dict(schema='invented_authored_source_receipts_v1',invented=True,
        operation_id=manifest['operation_id'],manifest_file_sha256=subject.envelope.sha(raw(manifest)),rows=rows,camera_commands=[])
    args['ordinary_buffers']['authored_source_receipts']=raw(receipts)
    return make_source_anchor(args,dependency_anchor)


def make_source_anchor(args,dependency_anchor):
    return dict(schema='invented_authored_source_anchor_v1',invented=True,
        operation_id=dependency_anchor['operation_id'],
        manifest_file_sha256=subject.envelope.sha(args['ordinary_buffers']['authored_source_manifest']),
        receipts_file_sha256=subject.envelope.sha(args['ordinary_buffers']['authored_source_receipts']),
        dependency_anchor_file_sha256=subject.envelope.sha(raw(dependency_anchor)))


def fixture():
    c,args,dep_anchor=dependency_fixture();basis=basis_fixture()
    for role in subject.links.INPUTS:args['ordinary_buffers'][role]=basis['ordinary_buffers'][role]
    c['protected']=basis['candidate']['protected']
    anchor=add_source_records(c,args,dep_anchor)
    return c,args,dep_anchor,anchor


def bind(c,args,dep_anchor,anchor,*,composed=False,external=None):
    c=copy.deepcopy(c)
    c['sources']={n:subject.envelope.receipt(v) for n,v in args['source_buffers'].items()}
    c['ordinary']={n:subject.envelope.receipt(v) for n,v in args['ordinary_buffers'].items()}
    docs=chain(c)
    kwargs=dict(external_seal_sha256=subject.envelope.sha(docs['seal']),**args,
        source_anchor_bytes=raw(anchor),external_source_anchor_sha256=external or subject.envelope.sha(raw(anchor)),
        dependency_anchor_bytes=raw(dep_anchor))
    if composed:
        return subject.validate_invented_composed_inputs(docs,**kwargs,
            external_dependency_anchor_sha256=subject.envelope.sha(raw(dep_anchor)))
    return subject.validate_invented_source_roles(docs,**kwargs)


def change(args,role,mutate):
    value=subject.envelope.decode(args['ordinary_buffers'][role]);mutate(value)
    args['ordinary_buffers'][role]=raw(value)


def reanchor(args,dep_anchor):
    change(args,'authored_source_receipts',lambda v:v.update(
        manifest_file_sha256=subject.envelope.sha(args['ordinary_buffers']['authored_source_manifest'])))
    return make_source_anchor(args,dep_anchor)


class SourceReceiptTests(unittest.TestCase):
    def test_complete_claims_remain_unobserved_without_io(self):
        c,args,dep,anchor=fixture();before=copy.deepcopy((c,args,dep,anchor))
        result=bind(c,args,dep,anchor)
        self.assertEqual(result['source_roles_checked'],44)
        self.assertEqual(result['checked_roles'],sorted(subject.SOURCE_INPUTS))
        for key in ('source_reads_observed','source_origin_authenticated','source_freshness_verified','execution_authorized'):
            self.assertIs(result[key],False)
        self.assertEqual((c,args,dep,anchor),before)

    def test_external_anchor_cannot_be_changed(self):
        c,args,dep,anchor=fixture()
        with self.assertRaisesRegex(ValueError,'source_external_anchor'):bind(c,args,dep,anchor,external='0'*64)

    def test_original_manifest_bytes_not_canonical_object(self):
        c,args,dep,anchor=fixture();args['ordinary_buffers']['authored_source_manifest']+=b'\n'
        with self.assertRaisesRegex(ValueError,'source_original_bytes'):bind(c,args,dep,anchor)

    def test_rebound_anchor_does_not_repair_stale_receipt_manifest(self):
        c,args,dep,anchor=fixture();args['ordinary_buffers']['authored_source_manifest']+=b'\n'
        anchor=make_source_anchor(args,dep)
        with self.assertRaisesRegex(ValueError,'source_receipt_manifest'):bind(c,args,dep,anchor)

    def test_dependency_anchor_is_bound_as_original_bytes(self):
        c,args,dep,anchor=fixture();dep['prior_review_sha256']='c'*64
        with self.assertRaisesRegex(ValueError,'source_original_bytes'):bind(c,args,dep,anchor)

    def test_all_sidecar_operations_agree(self):
        for role in ('authored_source_manifest','authored_source_receipts'):
            c,args,dep,anchor=fixture();change(args,role,lambda v:v.update(operation_id='different'))
            with self.subTest(role=role),self.assertRaisesRegex(ValueError,'source_cross_operation'):
                bind(c,args,dep,reanchor(args,dep))

    def test_roster_must_include_host_and_every_source(self):
        for role in ('host_parent_adapter','bound.role:core'):
            c,args,dep,anchor=fixture();change(args,'authored_source_manifest',lambda v:v['sources'].pop(role))
            with self.subTest(role=role),self.assertRaisesRegex(ValueError,'source_manifest_roster'):
                bind(c,args,dep,reanchor(args,dep))

    def test_receipt_rows_require_exact_roster(self):
        c,args,dep,anchor=fixture();change(args,'authored_source_receipts',lambda v:v['rows'].pop('host_parent_adapter'))
        with self.assertRaisesRegex(ValueError,'source_receipt_roster'):bind(c,args,dep,reanchor(args,dep))

    def test_external_anchor_cannot_refer_to_current_envelope_documents(self):
        c,args,dep,anchor=fixture()
        c['sources']={n:subject.envelope.receipt(v) for n,v in args['source_buffers'].items()}
        c['ordinary']={n:subject.envelope.receipt(v) for n,v in args['ordinary_buffers'].items()}
        docs=chain(c)
        for field in ('manifest_file_sha256','receipts_file_sha256','dependency_anchor_file_sha256'):
            for name in docs:
                with self.subTest(field=field,name=name),self.assertRaisesRegex(ValueError,'source_anchor_cycle'):
                    bind(c,args,dep,dict(anchor,**{field:subject.envelope.sha(docs[name])}))

    def test_anchor_operation_cannot_replace_sidecar_context(self):
        c,args,dep,anchor=fixture();anchor['operation_id']='different'
        with self.assertRaisesRegex(ValueError,'source_cross_operation'):bind(c,args,dep,anchor)

    def test_sidecars_and_anchor_are_closed_invented_records(self):
        for name in ('authored_source_manifest','authored_source_receipts','anchor'):
            for field,value in (('extra',True),('invented',False)):
                c,args,dep,anchor=fixture()
                if name=='anchor':anchor[field]=value
                else:
                    change(args,name,lambda v:v.update({field:value}));anchor=reanchor(args,dep)
                with self.subTest(name=name,field=field),self.assertRaises(ValueError):bind(c,args,dep,anchor)

    def test_protected_bytes_cannot_join_source_roster(self):
        c,args,dep,anchor=fixture();change(args,'authored_source_manifest',lambda v:v['sources'].update(firmware_package={}))
        with self.assertRaisesRegex(ValueError,'source_manifest_roster'):bind(c,args,dep,reanchor(args,dep))

    def test_changed_source_bytes_not_repaired_by_envelope_rebinding(self):
        c,args,dep,anchor=fixture();args['source_buffers']['host_parent_adapter']=b'# drift'
        with self.assertRaisesRegex(ValueError,'source_buffer_identity'):bind(c,args,dep,anchor)

    def test_wrong_role_path_even_when_other_receipts_agree(self):
        c,args,dep,anchor=fixture();role='bound.role:core'
        def manifest(v):v['sources'][role]['path']='private/rebound/core.py'
        def receipts(v):v['rows'][role]['receipt']['path']='D:/invented-root/private/rebound/core.py'
        change(args,'authored_source_manifest',manifest);change(args,'authored_source_receipts',receipts)
        with self.assertRaisesRegex(ValueError,'source_qualified_binding'):bind(c,args,dep,reanchor(args,dep))

    def test_protected_label_alias_and_case_collision(self):
        for path in ('private/invented-constants.py','private/INVENTED-ROLES/CORE.py'):
            c,args,dep,anchor=fixture();change(args,'authored_source_manifest',lambda v:
                v['sources']['host_parent_adapter'].update(path=path))
            with self.subTest(path=path),self.assertRaises(ValueError):bind(c,args,dep,reanchor(args,dep))

    def test_declared_read_completion_is_closed_and_strict(self):
        for field,value in (('closed',False),('close_attempts',True),('close_attempts',2),('eof_probes',0),
            ('eof_probes',None),('read_calls',True),
            ('read_calls',1),('read_calls',1000000)):
            c,args,dep,anchor=fixture();change(args,'authored_source_receipts',lambda v:
                v['rows']['host_parent_adapter'].update({field:value}))
            with self.subTest(field=field,value=value),self.assertRaisesRegex(ValueError,'source_read_completion'):
                bind(c,args,dep,reanchor(args,dep))

    def test_stat_stability_and_expected_identity(self):
        for stamp,key,value in (('fstat_after','mtime_ns',9),('lstat_after','inode',8),
            ('fstat_before','nlink',2),('lstat_before','file_attributes',0x400),('fstat_after','size',1)):
            c,args,dep,anchor=fixture();change(args,'authored_source_receipts',lambda v:
                v['rows']['host_parent_adapter']['receipt'][stamp].update({key:value}))
            with self.subTest(stamp=stamp,key=key),self.assertRaises(ValueError):bind(c,args,dep,reanchor(args,dep))

    def test_cross_api_ctime_and_attributes_need_not_be_equal(self):
        c,args,dep,anchor=fixture()
        def mutate(v):
            for name in ('fstat_before','fstat_after'):
                v['rows']['host_parent_adapter']['receipt'][name].update(ctime_ns=999,file_attributes=1)
        change(args,'authored_source_receipts',mutate)
        self.assertFalse(bind(c,args,dep,reanchor(args,dep))['source_reads_observed'])

    def test_aliased_physical_identity_refuses(self):
        c,args,dep,anchor=fixture()
        def mutate(v):v['sources']['host_parent_adapter']['identity']=dict(v['sources']['outer_gate']['identity'])
        change(args,'authored_source_manifest',mutate)
        with self.assertRaises(ValueError):bind(c,args,dep,reanchor(args,dep))

    def test_rebound_receipts_cannot_hide_physical_identity_alias(self):
        c,args,dep,anchor=fixture()
        manifest=subject.envelope.decode(args['ordinary_buffers']['authored_source_manifest'])
        pair={k:manifest['sources']['outer_gate']['identity'][k] for k in ('device','inode')}
        change(args,'authored_source_manifest',lambda v:v['sources']['host_parent_adapter']['identity'].update(pair))
        def mutate(v):
            for stamp in ('lstat_before','fstat_before','fstat_after','lstat_after'):
                v['rows']['host_parent_adapter']['receipt'][stamp].update(pair)
        change(args,'authored_source_receipts',mutate)
        with self.assertRaisesRegex(ValueError,'source_identity_alias'):bind(c,args,dep,reanchor(args,dep))

    def test_invalid_source_fails_before_any_retained_execution(self):
        c,args,dep,anchor=fixture();args['source_buffers']['host_parent_adapter']=b'# drift'
        with patch.object(subject.basis,'validate_invented_basis_roles') as basis:
            with self.assertRaises(ValueError):bind(c,args,dep,anchor,composed=True)
            basis.assert_not_called()

    def test_composition_calls_both_retained_apis_on_same_buffers(self):
        c,args,dep,anchor=fixture()
        with patch.object(subject.basis,'validate_invented_basis_roles',return_value={'invented_stub':True}) as basis:
            result=bind(c,args,dep,anchor,composed=True)
        self.assertEqual(len(result['checked_roles']),10)
        self.assertEqual(len(result['pending_ordinary_roles']),4)
        self.assertEqual(result['dependency_result']['checked_roles'],['dependency_fixed','dependency_packet'])
        self.assertIs(basis.call_args.kwargs['source_buffers'],args['source_buffers'])
        self.assertIs(result['dependency_bridge_verified'],False)

    def test_dependency_refusal_precedes_owned_basis_execution(self):
        c,args,dep,anchor=fixture();args['ordinary_buffers']['dependency_fixed']=b'{}'
        with patch.object(subject.basis,'validate_invented_basis_roles') as basis:
            with self.assertRaisesRegex(ValueError,'dependency_fixed_original_bytes'):
                bind(c,args,dep,anchor,composed=True)
            basis.assert_not_called()

    def test_runtime_always_refuses(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):subject.run_runtime()
