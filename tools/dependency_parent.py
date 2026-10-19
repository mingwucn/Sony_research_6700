"""Strict saved controller/dependency reconciliation; no activation API.

Only ordinary metadata is read. Consistent caller-owned records do not prove
producer identity, historical truth, runtime compatibility or execution consent.
"""
import json
import math
from pathlib import Path

from tools import dependency_evidence as core
from tools import dependency_execution as execution
from tools import dependency_producer as producer


BRIDGE = ('controller-result.json', 'completion.json')


def _controller_json(raw):
    """Retained controller grammar: finite nonnegative floats in *seconds fields.

    Other metadata continues using the dependency grammar, which rejects floats.
    The controller's own semantic validator remains responsible for its schema.
    """
    def pairs(rows):
        value = {}
        for key, item in rows:
            core._need(key not in value, 'duplicate_key')
            value[key] = item
        return value

    def invalid(value):
        raise core.EvidenceError('json_number')

    value = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=invalid)
    nodes = 0

    def visit(item, key='', depth=0):
        nonlocal nodes
        nodes += 1
        core._need(nodes <= 4096 and depth <= 32, 'parent_json_bound')
        if type(item) is float:
            core._need(key.endswith('seconds') and math.isfinite(item) and item >= 0, 'json_number')
        elif type(item) is dict:
            for name, child in item.items():
                visit(child, name, depth+1)
        elif type(item) is list:
            for child in item:
                visit(child, '', depth+1)

    visit(value)
    return value


def _hashes(value, names):
    core._shape(value, names)
    for digest in value.values():
        core._digest(digest)


def validate_saved_controller(*, folder, inputs, operation_id, stdout,
                              stdout_sha256, dependency_sha256, bridge_sha256,
                              invented=True):
    """Recompute all eleven dependency artifacts and both bridge envelopes.

    Read the start record independently, bind the operation to the original
    inputs, compare summary JSON values and hash the exact captured stdout.
    No observer, factory, protected-source loader or process action is accepted.
    Runtime record grammar remains a consistency check, never an activation.
    """
    core._need(type(invented) is bool, 'collection_mode')
    policy, _, _, _, _ = producer.bind_inputs(**inputs)
    core._need(type(operation_id) is str and operation_id == policy['operation_id'], 'parent_operation')
    core._digest(stdout_sha256)
    core._need(type(stdout) is bytes and 0 < len(stdout) <= 16384, 'parent_stdout_bound')
    core._need(producer.sha(stdout) == stdout_sha256, 'parent_stdout_hash')
    summary = _controller_json(stdout)
    core._need(type(summary) is dict and type(summary.get('script_exit_code')) is int and
               summary['script_exit_code'] == 0, 'parent_summary')
    _hashes(bridge_sha256, BRIDGE)
    folder = Path(folder)
    core._need(set(path.name for path in folder.iterdir()) == set(BRIDGE)|{'started.json', 'collected'},
               'parent_bridge_roster')
    start_raw, _ = producer.read_verified(str(folder/'started.json'), limit=2*1024**2)
    start = core._json_text(start_raw.decode('utf-8'))
    prefix = 'invented_' if invented else ''
    expected_start = dict(schema=prefix+'collected_controller_started_v1', operation_id=operation_id,
        expectation_sha256=core._hash(policy), test_injection_used=invented, automatic_retry=False,
        protected_input_authorized=False, camera_commands=[])
    core._need(core._canonical(start) == core._canonical(expected_start), 'parent_start')
    dependency = execution.validate_saved_composition(folder/'collected', inputs, invented=invented)
    _hashes(dependency_sha256, dependency)
    core._need(core._canonical(dependency) == core._canonical(dependency_sha256), 'parent_dependency_hashes')
    bridge_raw = {name:producer.read_verified(str(folder/name), limit=2*1024**2)[0] for name in BRIDGE}
    bridge = {name:producer.sha(raw) for name,raw in bridge_raw.items()}
    core._need(core._canonical(bridge) == core._canonical(bridge_sha256), 'parent_bridge_hashes')
    result = _controller_json(bridge_raw['controller-result.json'])
    core._shape(result, ('code','summary','test_injection_used','camera_commands'))
    core._need(type(result['code']) is int and result['code'] == 0 and
               result['test_injection_used'] is invented and result['camera_commands'] == [], 'parent_result')
    core._need(core._canonical(result['summary']) == core._canonical(summary), 'parent_summary')
    dependency_raw, _ = producer.read_verified(str(folder/'collected/completion.json'), limit=4*1024**2)
    core._need(producer.sha(dependency_raw) == dependency['completion.json'], 'parent_dependency_changed')
    dependency_completion = core._json_text(dependency_raw.decode('utf-8'))
    expected_complete = dict(schema=prefix+'collected_controller_completion_v1',
        status=prefix+'collected_controller_complete', controller_entered=True, callback_released=True,
        dependency_completion_sha256=core._hash(dependency_completion), test_injection_used=invented,
        automatic_retry=False, actual_dependency_observation_performed=not invented,
        execution_authorized=False, feature_supported=False, recovery_proven=False,
        device_write_gate_passed=False, camera_commands=[])
    completion = core._json_text(bridge_raw['completion.json'].decode('utf-8'))
    core._need(core._canonical(completion) == core._canonical(expected_complete), 'parent_completion')
    return dict(schema='collected_controller_saved_verification_v1', status='consistent_saved_controller',
        operation_id=operation_id, stdout_sha256=stdout_sha256, start_sha256=producer.sha(start_raw),
        dependency_sha256=dependency, bridge_sha256=bridge, test_injection_used=invented,
        producer_execution_authenticated=False, actual_runtime_verified=False, historical_truth_verified=False,
        operational_acceptance=False, execution_authorized=False, feature_supported=False,
        recovery_proven=False, device_write_gate_passed=False, camera_commands=[])


def main():
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
