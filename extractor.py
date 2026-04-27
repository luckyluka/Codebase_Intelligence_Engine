import ast
import hashlib


def extract_imports(path, source):
    """
    Returns structured imports:
    [
        {"type": "...", "target": "..."}
    ]
    """
    imports = []

    try:
        tree = ast.parse(source)
    except Exception:
        return imports

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    "type": "local_or_external",
                    "target": alias.name.split(".")[0]
                })

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append({
                    "type": "local_or_external",
                    "target": node.module.split(".")[0]
                })

    return imports

def _get_source_segment(source_lines, node):
    """Extract function body from source using line numbers"""
    start = node.lineno - 1
    end = getattr(node, "end_lineno", node.lineno)
    return "\n".join(source_lines[start:end])


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_functions(source: str):
    functions = []

    try:
        tree = ast.parse(source)
        source_lines = source.splitlines()
    except Exception:
        return functions

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):

            body = _get_source_segment(source_lines, node)

            functions.append({
                "name": node.name,
                "lineno": node.lineno,
                "end_lineno": getattr(node, "end_lineno", node.lineno),
                "args": [arg.arg for arg in node.args.args],

                # NEW FIELDS (3.2 core)
                "body": body,
                "hash": _hash(body)
            })

    return functions