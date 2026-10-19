"""Invented document chains; no paths, sockets or protected inputs."""
import copy
import json
import unittest

from tools import dependency_authority_grammar as grammar
from tests.test_dependency_operational_scope import fixture as scope_fixture


def raw(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def fixture(phase='prepared'):
    sources = {role: ('# invented ' + role).encode() for role in grammar.SOURCE_ROLES}
    ordinary = {role: b'{}' for role in grammar.policy.ORDINARY_INPUTS}
    history = {role: ('invented history ' + role).encode() for role in grammar.HISTORY_ROLES}
    ordinary['historical_evidence_index'] = raw(dict(schema='invented_historical_index_v1',
        invented=True, purpose='comparison_only', receipts={r: grammar.receipt(v) for r, v in history.items()}))
    scope = raw(scope_fixture())
    candidate = dict(schema='invented_authority_candidate_v1', invented=True, phase=phase,
        scope_file_sha256=grammar.sha(scope),
        sources={r: grammar.receipt(v) for r, v in sources.items()},
        ordinary={r: grammar.receipt(v) for r, v in ordinary.items()},
        protected={r: dict(bytes=123, sha256='a'*64, read_authorized=False) for r in grammar.PROTECTED},
        historical_blockers=list(grammar.policy.HISTORY), rights_uncertainties=sorted(grammar.policy.RIGHTS),
        runtime=dict(interpreter_identity='invented-python', argv=['invented-python', '-I', '-S', '-B', '-X', 'utf8', '-c', '# invented']))
    args = dict(scope_bytes=scope, source_buffers=sources, ordinary_buffers=ordinary, historical_buffers=history)
    return candidate, args


def chain(candidate, review_outcome='accepted_shape'):
    docs = dict(candidate=raw(candidate))
    docs['review'] = raw(dict(schema='invented_authority_review_v1', invented=True,
        candidate_sha256=grammar.sha(docs['candidate']), outcome=review_outcome))
    docs['decision'] = raw(dict(schema='invented_authority_decision_v1', invented=True,
        candidate_sha256=grammar.sha(docs['candidate']), review_sha256=grammar.sha(docs['review']),
        outcome='pending' if candidate['phase']=='prepared' else 'accepted_shape'))
    docs['seal'] = raw(dict(schema='invented_authority_seal_v1', invented=True,
        **{name+'_sha256': grammar.sha(docs[name]) for name in ('candidate','review','decision')}))
    return docs


class AuthorityGrammarTests(unittest.TestCase):
    def check(self, candidate, args, **kwargs):
        docs = chain(candidate, **kwargs)
        return grammar.validate_invented_chain(docs, external_seal_sha256=grammar.sha(docs['seal']), **args)

    def refuses(self, mutate):
        candidate, args = fixture()
        mutate(candidate, args)
        with self.assertRaises(ValueError):
            self.check(candidate, args)

    def test_prepared_and_operational_shape_never_authorize(self):
        for phase in ('prepared', 'operational_shape'):
            candidate, args = fixture(phase)
            before = copy.deepcopy((candidate, args))
            result = self.check(candidate, args)
            self.assertEqual((candidate, args), before)
            self.assertEqual(result['phase'], phase)
            for key in ('execution_authorized', 'runtime_qualified', 'protected_inputs_read',
                        'feature_supported', 'recovery_proven', 'device_write_gate_passed'):
                self.assertIs(result[key], False)

    def test_missing_or_extra_document(self):
        c, a = fixture()
        for docs in ({k:v for k,v in chain(c).items() if k!='review'}, dict(chain(c), authority=b'{}')):
            with self.assertRaises(ValueError):
                grammar.validate_invented_chain(docs, external_seal_sha256='a'*64, **a)

    def test_actual_schema_or_invented_false_refuses(self):
        self.refuses(lambda c,a: c.update(invented=False))
        self.refuses(lambda c,a: c.update(schema='operational_authority_candidate_v1'))

    def test_external_anchor_cannot_be_self_declared(self):
        c,a = fixture(); docs = chain(c)
        with self.assertRaisesRegex(ValueError, 'external_anchor'):
            grammar.validate_invented_chain(docs, external_seal_sha256='0'*64, **a)
        self.refuses(lambda c,a: c.update(external_seal_sha256='a'*64))

    def test_same_object_reformatted_bytes_fail_binding(self):
        c,a = fixture(); docs = chain(c)
        docs['candidate'] = json.dumps(c, indent=2).encode()
        with self.assertRaisesRegex(ValueError, 'review_binding'):
            grammar.validate_invented_chain(docs, external_seal_sha256=grammar.sha(docs['seal']), **a)

    def test_all_document_edges_bound_to_original_bytes(self):
        c,a = fixture()
        for name in ('review','decision','seal'):
            docs = chain(c); value = json.loads(docs[name]); value['candidate_sha256']='b'*64
            docs[name] = raw(value)
            with self.subTest(name=name), self.assertRaises(ValueError):
                grammar.validate_invented_chain(docs, external_seal_sha256=grammar.sha(docs['seal']), **a)

    def test_cycles_and_unknown_fields_refuse(self):
        self.refuses(lambda c,a: c.update(seal_sha256='a'*64))
        self.refuses(lambda c,a: c.update(execution_authorized=True))

    def test_source_content_change_or_missing_role(self):
        self.refuses(lambda c,a: a['source_buffers'].update(outer_gate=b'changed'))
        self.refuses(lambda c,a: c['sources'].pop('host_parent_adapter'))

    def test_source_canonical_digest_cannot_substitute_file_digest(self):
        self.refuses(lambda c,a: c['sources']['outer_gate'].update(sha256='a'*64))

    def test_scope_change_even_when_rebound_refuses(self):
        def change(c,a):
            scope=json.loads(a['scope_bytes']); scope['scope']['content_reads']=1
            a['scope_bytes']=raw(scope); c['scope_file_sha256']=grammar.sha(a['scope_bytes'])
        self.refuses(change)

    def test_scope_reformat_needs_original_byte_rebinding(self):
        self.refuses(lambda c,a: a.update(scope_bytes=json.dumps(scope_fixture(),indent=2).encode()))

    def test_protected_never_accepted_as_ordinary_buffers(self):
        for role in grammar.PROTECTED:
            self.refuses(lambda c,a: a['ordinary_buffers'].update({role:b'invented'}))
            self.refuses(lambda c,a: c['protected'][role].update(read_authorized=True))

    def test_historical_receipt_changes_and_limit_removal_refuse(self):
        self.refuses(lambda c,a: a['historical_buffers'].update(q_old_seal=b'changed history'))
        self.refuses(lambda c,a: c['historical_blockers'].pop())
        self.refuses(lambda c,a: c['rights_uncertainties'].pop())

    def test_opaque_ordinary_receipt_is_not_a_freshness_assertion(self):
        c,a=fixture()
        a['ordinary_buffers']['basis']=a['historical_buffers']['q_old_seal']
        c['ordinary']['basis']=grammar.receipt(a['ordinary_buffers']['basis'])
        self.assertFalse(self.check(c,a)['execution_authorized'])

    def test_history_index_cannot_claim_current_authority(self):
        def change(c,a):
            index=json.loads(a['ordinary_buffers']['historical_evidence_index']); index['purpose']='current_authority'
            a['ordinary_buffers']['historical_evidence_index']=raw(index)
            c['ordinary']['historical_evidence_index']=grammar.receipt(a['ordinary_buffers']['historical_evidence_index'])
        self.refuses(change)

    def test_review_refusal(self):
        c,a=fixture()
        with self.assertRaisesRegex(ValueError,'decision_refused'):
            self.check(c,a,review_outcome='refused_shape')

    def test_prepared_decision_cannot_be_operational(self):
        c,a=fixture(); docs=chain(c); decision=json.loads(docs['decision']); decision['outcome']='accepted_shape'
        docs['decision']=raw(decision)
        seal=json.loads(docs['seal']); seal['decision_sha256']=grammar.sha(docs['decision']); docs['seal']=raw(seal)
        with self.assertRaisesRegex(ValueError,'decision_refused'):
            grammar.validate_invented_chain(docs,external_seal_sha256=grammar.sha(docs['seal']),**a)

    def test_duplicate_json_keys_and_nonfinite_refuse(self):
        for value in (b'{"schema":1,"schema":2}', b'{"value":NaN}', b'{"value":Infinity}', b'{"value":1e999}', b'\xff'):
            with self.subTest(value=value), self.assertRaises(ValueError): grammar.decode(value)

    def test_integer_receipt_does_not_accept_boolean(self):
        self.refuses(lambda c,a: c['sources']['outer_gate'].update(bytes=True))

    def test_runtime_argv_and_fields_cannot_expand(self):
        self.refuses(lambda c,a: c['runtime']['argv'].insert(1,'-m'))
        self.refuses(lambda c,a: c['runtime'].update(observer='injected'))

    def test_runtime_disabled(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'): grammar.run_runtime()

    def test_raw_document_bounds_and_types(self):
        for value in ('{}', b'', b' '*(grammar.MAX_BYTES+1)):
            with self.subTest(kind=type(value)), self.assertRaises(ValueError): grammar.decode(value)


if __name__ == '__main__':
    unittest.main()
