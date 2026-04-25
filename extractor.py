import ast


def extract_imports(file_path: str):
    """
    Extract Python imports using AST.
    Deterministic, no heuristics.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)

    imports = []

    for node in ast.walk(tree):
        # import x
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)

        # from x import y
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for n in node.names:
                if module:
                    imports.append(f"{module}.{n.name}")
                else:
                    imports.append(n.name)

    return imports