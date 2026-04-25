import os
import json
from extractor import extract_imports


IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    "dist",
    "build"
}

IGNORE_EXTENSIONS = {
    ".pyc",
    ".DS_Store"
}


def should_ignore(path: str) -> bool:
    parts = set(path.split(os.sep))

    if any(part in IGNORE_DIRS for part in parts):
        return True

    if any(path.endswith(ext) for ext in IGNORE_EXTENSIONS):
        return True

    return False


def detect_language(path: str) -> str:
    if path.endswith(".py"):
        return "python"
    if path.endswith(".js"):
        return "javascript"
    if path.endswith(".ts"):
        return "typescript"
    if path.endswith(".c"):
        return "c"
    if path.endswith(".h"):
        return "c"
    if path.endswith(".md"):
        return "markdown"
    if path.endswith(".json"):
        return "json"
    return "unknown"


def scan_directory(root="."):
    results = []

    for dirpath, dirnames, filenames in os.walk(root):

        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

        for file in filenames:
            full_path = os.path.join(dirpath, file)

            if should_ignore(full_path):
                continue

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                content = ""

            file_data = {
                "path": full_path,
                "size": len(content),
                "modified_at": os.path.getmtime(full_path),
                "language": detect_language(full_path),
                "imports": extract_imports(full_path, content)
            }

            results.append(file_data)

    return results


def save_structure(output_path="structure.json", root="."):
    data = scan_directory(root)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return data