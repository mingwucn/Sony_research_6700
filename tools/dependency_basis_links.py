"""Pure invented metadata links. Supplied recomputations are not proof of execution."""
if __name__ == '__main__':
    raise SystemExit(2)

from tools import dependency_authority_grammar as contract
from tools import dependency_outer_contract as outer

ROLES = frozenset(outer.ROLES)
INPUTS = frozenset(('basis','source_manifest','prerequisites','role_authority','binding_schema','binding_plan'))


def equal(left, right):
    # Canonical JSON distinguishes bool from int, unlike Python equality.
    return contract.policy.encoded(left) == contract.policy.encoded(right)


def private_path(value):
    contract.need(type(value) is str and value.startswith('private/') and
        len(value) <= 512 and all(ord(c) >= 32 and ord(c) != 127 for c in value) and
        not any(c in value for c in '\\:<>"|?*'), 'private_path')
    reserved={'CON','PRN','AUX','NUL','CONIN$','CONOUT$','CLOCK$'} | {
        p+n for p in ('COM','LPT') for n in tuple(str(i) for i in range(1,10))+('¹','²','³')}
    contract.need(all(part not in ('','.','..') and not part.endswith(('.', ' ')) and
        part.split('.')[0].upper() not in reserved for part in value.split('/')), 'private_path')


def validate_invented_basis_links(*, candidate, ordinary_buffers, source_buffers,
                                  recomputed_plan, frozen_basis, retained_schema):
    """Compare six role records to externally recomputed pure-validator outputs.

    Caller must separately validate the full envelope and own the recomputers.
    This pure API authenticates neither supplied outputs nor source execution.
    Paths here are identity labels only; nothing is opened or executed.
    """
    contract.shape(ordinary_buffers, contract.policy.ORDINARY_INPUTS, 'ordinary_roster')
    contract.shape(source_buffers, contract.SOURCE_ROLES, 'source_roster')
    data={name:contract.decode(ordinary_buffers[name]) for name in INPUTS}
    basis=data['basis']; manifest=data['source_manifest']; prerequisites=data['prerequisites']
    contract.shape(basis, contract.policy.BASIS_ROLES, 'basis_roster')
    contract.need(equal(frozen_basis,basis), 'retained_basis_difference')
    contract.shape(manifest, ('schema','relative_path','bytes','sha256','readonly_required',
        'existing_private_acquisition','no_acquisition_or_download','camera_commands'), 'source_manifest_shape')
    contract.need(manifest['schema']=='gdt_io_source_manifest_v1' and
        type(manifest['bytes']) is int and 8<=manifest['bytes']<=2**31 and
        all(manifest[k] is True for k in ('readonly_required','existing_private_acquisition','no_acquisition_or_download'))
        and manifest['camera_commands']==[], 'source_manifest')
    private_path(manifest['relative_path']); contract.digest(manifest['sha256'])
    contract.shape(prerequisites, ('qualified_roles','binding_input','constants_relative_path',
        'constants_sha256','constants_assignment_count','selected_literal_lengths','crypto_python_relative_path'), 'prerequisite_shape')
    private_path(prerequisites['constants_relative_path'])
    private_path(prerequisites['crypto_python_relative_path'])
    contract.digest(prerequisites['constants_sha256'])
    contract.need(type(prerequisites['constants_assignment_count']) is int and
        prerequisites['constants_assignment_count']==15 and
        equal(prerequisites['selected_literal_lengths'],dict(common=16,candidate=32)), 'constants_shape')
    contract.need(len({manifest['relative_path'].casefold(), prerequisites['constants_relative_path'].casefold(),
        prerequisites['crypto_python_relative_path'].casefold()})==3, 'protected_path_alias')
    contract.shape(data['role_authority'], ('roles',), 'role_authority')
    roles=data['role_authority']['roles']; contract.shape(roles, ROLES, 'role_roster')
    contract.shape(prerequisites['binding_input'], ('schema','roles','dependency'), 'binding_input_shape')
    contract.need(prerequisites['binding_input']['schema']=='activation_binding_input_v1' and
        equal(prerequisites['qualified_roles'],roles) and equal(prerequisites['binding_input']['roles'],roles), 'role_cross_binding')
    paths={manifest['relative_path'].casefold(),prerequisites['constants_relative_path'].casefold(),
           prerequisites['crypto_python_relative_path'].casefold()}
    for role,row in roles.items():
        contract.shape(row, ('path','sha256'), 'role_shape'); private_path(row['path'])
        contract.digest(row['sha256'])
        contract.need(row['path'].endswith('.py') and row['path'].casefold() not in paths, 'role_path_alias')
        paths.add(row['path'].casefold())
        contract.need(contract.sha(source_buffers['bound.role:'+role])==row['sha256'], 'role_source_bytes')
    contract.need(equal(data['binding_schema'],retained_schema), 'retained_schema_difference')
    contract.need(equal(data['binding_plan'],recomputed_plan), 'retained_plan_difference')
    contract.need(all(recomputed_plan.get(k) is False for k in
        ('execution_authorized','actual_runtime_verified','actual_binding_ready')) and
        recomputed_plan.get('camera_commands')==[], 'plan_authority')
    contract.need(equal(recomputed_plan['roles'],roles) and
        equal(recomputed_plan['load_order'],retained_schema['load_order']) and
        equal(recomputed_plan['protected_order'],retained_schema['protected_order']), 'plan_order')
    contract.shape(candidate['protected'], contract.PROTECTED, 'protected_roster')
    for name,size,digest in (('firmware_package',manifest['bytes'],manifest['sha256']),
                            ('operational_constants',None,prerequisites['constants_sha256'])):
        row=candidate['protected'][name]
        contract.need(row['read_authorized'] is False and row['sha256']==digest and
            (size is None or row['bytes']==size), 'protected_identity')
    prior=basis['prior_stream']
    contract.need(type(prior) is dict and type(prior.get('input_package_bytes')) is int and
        prior['input_package_bytes']==manifest['bytes'] and prior.get('input_package_sha256')==manifest['sha256'], 'basis_source_identity')
    return dict(schema='invented_basis_links_v1', checked_link_roles=sorted(INPUTS),
        recomputation_authenticated=False, protected_inputs_read=False,
        execution_authorized=False, feature_supported=False, recovery_proven=False,
        device_write_gate_passed=False, camera_commands=[])


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
