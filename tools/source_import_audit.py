"""Static supplied-buffer import inventory, never an executing-code allowlist.

All branches and function bodies are scanned. No supplied module is imported,
compiled or executed. External names/hashes are caller claims; aliases, data flow,
embedded code strings, interpreter startup and stdlib dependencies are not proved.
"""
if __name__ == '__main__':
    raise SystemExit(2)

import ast
import hashlib
import re

NAME = re.compile(r'[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*\Z', re.ASCII)
MAX_SOURCE = 2 * 1024**2
MAX_TOTAL = 32 * 1024**2
MAX_NODES = 200000


def need(condition, code):
    if not condition:
        raise ValueError(code)


def audit_imports(buffers, *, roots, expected_hashes, stdlib_roots, namespace_packages=()):
    """Resolve a closed static import roster; refuse unknown/ambiguous imports.

    Namespace packages are explicitly source-free labels, never authenticated
    filesystem namespace observations. Every supplied leaf must be reachable.
    Call sites are syntax inventories, not execution or reachability evidence.
    """
    need(type(buffers) is dict and 0 < len(buffers) <= 128, 'source_roster')
    need(type(expected_hashes) is dict and set(expected_hashes) == set(buffers), 'hash_roster')
    need(type(roots) in (tuple, list) and roots and all(type(n) is str for n in roots) and
        len(set(roots)) == len(roots), 'root_roster')
    need(type(stdlib_roots) in (set, frozenset) and all(type(n) is str and NAME.fullmatch(n) and '.' not in n
        for n in stdlib_roots), 'stdlib_labels')
    need(type(namespace_packages) in (tuple, list) and all(type(n) is str for n in namespace_packages) and
        len(set(namespace_packages)) == len(namespace_packages),
        'namespace_roster')
    names = list(buffers) + list(namespace_packages)
    need(all(type(n) is str and len(n) <= 256 and NAME.fullmatch(n) for n in names), 'module_label')
    need(len({n.casefold() for n in names}) == len(names), 'module_alias')
    parents = {'.'.join(n.split('.')[:i]) for n in buffers for i in range(1,len(n.split('.')))}
    need(parents == set(namespace_packages), 'namespace_parents')
    need(not any(n.split('.')[0] in stdlib_roots for n in names), 'stdlib_shadow')
    need(all(type(n) is str and n in buffers for n in roots), 'root_missing')
    # Caller-owned mutable mappings are copied once. This is not a hostile-thread sandbox.
    sources = dict(buffers); hashes = dict(expected_hashes)
    total = 0; trees = {}; receipts = {}; nodes = 0
    for name, raw in sources.items():
        need(type(raw) is bytes and 0 < len(raw) <= MAX_SOURCE, 'source_bound')
        total += len(raw); need(total <= MAX_TOTAL, 'source_total_bound')
        digest = hashlib.sha256(raw).hexdigest()
        need(type(hashes[name]) is str and hashes[name] == digest, 'source_hash')
        try:
            tree = ast.parse(raw, filename='<source:'+name+'>')
        except (SyntaxError, ValueError, RecursionError) as error:
            raise ValueError('source_syntax') from error
        count = sum(1 for _ in ast.walk(tree)); nodes += count
        need(nodes <= MAX_NODES, 'source_node_bound')
        trees[name] = tree; receipts[name] = dict(bytes=len(raw), sha256=digest)
    graph = {n:set() for n in sources}; external = []; calls = []

    def resolve(owner, module, line):
        if module in sources:
            graph[owner].add(module)
        elif module.split('.')[0] in stdlib_roots:
            external.append(dict(owner=owner, module=module, line=line))
        else:
            raise ValueError('unresolved_import:'+owner+':'+module)

    for owner, tree in trees.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    need(alias.name not in namespace_packages, 'bare_namespace_import')
                    resolve(owner, alias.name, node.lineno)
            elif isinstance(node, ast.ImportFrom):
                need(node.level == 0 and node.module is not None, 'relative_import')
                need(all(a.name != '*' for a in node.names), 'star_import')
                if node.module in namespace_packages:
                    for alias in node.names:
                        resolve(owner, node.module+'.'+alias.name, node.lineno)
                else:
                    # from-leaf symbols can trigger implicit submodule loading;
                    # this inventory has no package/symbol execution semantics.
                    need(node.module not in sources, 'authored_symbol_import')
                    resolve(owner, node.module, node.lineno)
            elif isinstance(node, ast.Call):
                try:
                    expression = ast.unparse(node.func)
                except RecursionError as error:
                    raise ValueError('source_expression_depth') from error
                need(len(expression) <= 4096, 'source_expression_bound')
                calls.append(dict(owner=owner, line=node.lineno, column=node.col_offset,
                    expression=expression))
    order = []; active = set(); seen = set()

    def visit(name):
        need(name not in active, 'import_cycle')
        if name in seen:
            return
        active.add(name)
        for child in sorted(graph[name]):
            visit(child)
        active.remove(name); seen.add(name); order.append(name)

    for name in roots:
        visit(name)
    need(seen == set(sources), 'unreachable_source')
    return dict(schema='static_authored_import_inventory_v1', roots=list(roots), sources=receipts,
        namespaces=list(namespace_packages), dependency_order=order,
        authored_edges={n:sorted(graph[n]) for n in sorted(graph)},
        external_imports=sorted(external, key=lambda x:(x['owner'],x['line'],x['module'])),
        syntactic_calls=sorted(calls, key=lambda x:(x['owner'],x['line'],x['column'])),
        complete_static_import_roster=True, all_branches_scanned=True,
        dynamic_alias_dataflow_analyzed=False, embedded_code_strings_analyzed=False,
        external_import_closure_verified=False, namespace_origin_authenticated=False,
        source_origin_authenticated=False, execution_closure_verified=False,
        interpreter_startup_verified=False, validator_execution_owned=False,
        actual_inputs_accessed=False, execution_authorized=False,
        feature_supported=False, recovery_proven=False, device_write_gate_passed=False, camera_commands=[])


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
