import ast


STD_LIB = {
    "os", "sys", "json", "math", "time", "re",
    "datetime", "typing", "pathlib", "collections"
}


def classify(module_name: str):
    base = module_name.split(".")[0]

    if base in STD_LIB:
        return {"type": "stdlib", "target": module_name}

    return {"type": "local_or_external", "target": module_name}


def extract_imports(file_path: str, source: str):

    if not file_path.endswith(".py"):
        return []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    imports = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(classify(n.name))

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.append(classify(module))

    return imports