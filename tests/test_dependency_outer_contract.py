"""Invented request/terminal schema checks; no files, network or device I/O."""
import copy
from pathlib import Path
import unittest

from tools import dependency_outer_contract as contract


def request_fixture():
    folder = Path.cwd() / 'invented-never-created'
    def row(name):
        return dict(path=str(folder / name), size=1, sha256='a'*64,
                    lstat={}, fstat={})
    request = dict(schema='invented_successor_outer_request_v1',
        operation_id='1'*32, sources={n: row(str(i)+'.py')
            for i, n in enumerate(sorted(contract.SOURCE_ROLES))},
        packet=row('packet.json'), folder=str(folder),
        argv_prefix=['invented-python','-I','-S','-B','-X','utf8','-c','pass'],
        expected_runtime={'executable':'invented-python'},
        bootstrap_sha256=contract.sha(b'pass'), review_sha256='b'*64)
    request['authority'] = contract.authority(request)
    return request


def terminal_fixture(request, success=True):
    result = dict(schema='invented_successor_outer_child_v1',
        operation_id=request['operation_id'],
        status='invented_outer_child_complete' if success else 'needs_review',
        source_closure_sha256=contract.sha(contract.canonical(request['sources'])),
        neutral_namespace='_a6700_successor', source_roles=list(contract.CHILD),
        namespace_closed=True, role_loader_closed=True,
        metrics=dict(zip(contract.METRICS, (2,2,4,1,1,1))),
        test_injection_used=True, camera_commands=[],
        **dict.fromkeys(contract.FLAGS, False))
    if success:
        result.update(dependency_artifact_sha256=dict.fromkeys(contract.DEPENDENCY_ARTIFACTS,'c'*64),
            bridge_artifact_sha256=dict.fromkeys(('completion.json','controller-result.json'),'d'*64),
            summary_sha256='e'*64)
    else:
        result.update(failure_type='KeyboardInterrupt', cleanup_check_failed=False)
    return result


class ContractTests(unittest.TestCase):
    def test_closed_rosters(self):
        self.assertEqual(len(contract.SOURCE_ROLES),44)
        self.assertEqual(len(contract.CHILD),5)
        self.assertEqual(len(contract.DEPENDENCY_ARTIFACTS),11)

    def test_valid_invented_binding(self):
        request=request_fixture()
        self.assertIs(contract.validate_request(request),request)
        self.assertIs(request['authority']['execution_authorized'],False)

    def test_request_mutations_refused(self):
        original=request_fixture()
        mutations=[lambda r:r.update(extra=True),
            lambda r:r.update(schema='runtime_request'),
            lambda r:r.update(operation_id='2'*32),
            lambda r:r['sources'].pop('outer_child'),
            lambda r:r['authority'].update(execution_authorized=True),
            lambda r:r['authority'].update(camera_commands=['invented']),
            lambda r:r['argv_prefix'].__setitem__(1,'-i'),
            lambda r:r['argv_prefix'].__setitem__(-1,'print(1)'),
            lambda r:r['expected_runtime'].update(executable='other'),
            lambda r:r['packet'].update(path=str(Path.cwd()/'outside.json')),
            lambda r:r['packet'].update(size=True),
            lambda r:r['packet'].update(sha256='G'*64),
            lambda r:r['sources']['outer_child'].update(path=r['sources']['outer_entry']['path'])]
        for index,mutate in enumerate(mutations):
            with self.subTest(index=index):
                request=copy.deepcopy(original);mutate(request)
                with self.assertRaises(ValueError):contract.validate_request(request)

    def test_success_and_refusal_distinct(self):
        request=request_fixture()
        self.assertEqual(contract.validate_terminal(terminal_fixture(request),request),'success')
        self.assertEqual(contract.validate_terminal(terminal_fixture(request,False),request),'refused')

    def test_success_artifact_mutations_refused(self):
        request=request_fixture();original=terminal_fixture(request)
        mutations=[lambda r:r['dependency_artifact_sha256'].pop('completion.json'),
            lambda r:r['dependency_artifact_sha256'].update(extra='f'*64),
            lambda r:r['bridge_artifact_sha256'].update(**{'completion.json':'bad'}),
            lambda r:r.update(summary_sha256='z'*64),
            lambda r:r.update(namespace_closed=False),
            lambda r:r['metrics'].update(stream_opens=1),
            lambda r:r['metrics'].update(factory_calls=True),
            lambda r:r.update(operation_id='2'*32),
            lambda r:r.update(source_closure_sha256='0'*64),
            lambda r:r.update(source_roles=list(reversed(contract.CHILD)))]
        for index,mutate in enumerate(mutations):
            with self.subTest(index=index):
                result=copy.deepcopy(original);mutate(result)
                with self.assertRaises(ValueError):contract.validate_terminal(result,request)

    def test_authority_flags_never_promoted(self):
        request=request_fixture()
        for flag in contract.FLAGS:
            with self.subTest(flag=flag):
                result=terminal_fixture(request);result[flag]=True
                with self.assertRaises(ValueError):contract.validate_terminal(result,request)

    def test_refusal_cannot_carry_success_fields(self):
        request=request_fixture();result=terminal_fixture(request,False)
        result['summary_sha256']='a'*64
        with self.assertRaises(ValueError):contract.validate_terminal(result,request)

    def test_missing_and_unknown_terminal_refused(self):
        request=request_fixture()
        for result in (None,{},dict(status='unknown')):
            with self.subTest(result=result):
                with self.assertRaises(ValueError):contract.validate_terminal(result,request)

    def test_runtime_and_cli_disabled(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):contract.run_runtime()
        self.assertEqual(contract.main(),2)


if __name__=='__main__':
    unittest.main()
