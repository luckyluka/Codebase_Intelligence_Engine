import ast


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


def extract_functions(source):
    """
    Extract top-level function definitions with metadata
    """
    functions = []

    try:
        tree = ast.parse(source)
    except Exception:
        return functions

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "lineno": node.lineno,
                "end_lineno": getattr(node, "end_lineno", node.lineno),
                "args": [arg.arg for arg in node.args.args],
                "returns": None  # reserved for later
            })

    return functions