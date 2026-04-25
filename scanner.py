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

IGNORE_SUFFIXES = {
    ".pyc",
    ".pyo"
}

def scan_directory(root_path: str):
    files = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        # 🚫 prune directories in-place
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

        for f in filenames:
            if any(f.endswith(s) for s in IGNORE_SUFFIXES):
                continue

            full_path = os.path.join(dirpath, f)

            if os.path.isdir(full_path):
                continue

            file_info = {
                "path": full_path,
                "size": os.path.getsize(full_path),
                "modified_at": os.path.getmtime(full_path),
                "language": detect_language(full_path)
            }

            # ✅ PHASE 2.1 ADDITION
            if file_info["language"] == "python":
                try:
                    file_info["imports"] = extract_imports(full_path)
                except Exception:
                    file_info["imports"] = []
            else:
                file_info["imports"] = []

            files.append(file_info)

    return files


def detect_language(path: str):
    if path.endswith(".py"):
        return "python"
    elif path.endswith(".c") or path.endswith(".h"):
        return "c"
    elif path.endswith(".js"):
        return "javascript"
    elif path.endswith(".md"):
        return "markdown"
    return "unknown"