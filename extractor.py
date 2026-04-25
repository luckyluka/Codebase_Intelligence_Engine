# extractor.py
import ast
import os


STD_LIB = {
    "os", "sys", "json", "math", "time", "re", "datetime",
    "typing", "pathlib", "collections", "itertools"
}


def classify_import(module_name: str):
    if module_name.split(".")[0] in STD_LIB:
        return {"type": "stdlib", "target": module_name}

    return {"type": "external_or_local", "target": module_name}


import ast


def extract_imports(file_path: str, source: str):

    # ONLY parse Python files
    if not file_path.endswith(".py"):
        return []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        # malformed python file → skip safely
        return []

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append({
                    "type": "raw",
                    "target": n.name
                })

        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ""
            imports.append({
                "type": "raw",
                "target": module
            })

    return imports