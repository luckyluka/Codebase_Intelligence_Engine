import os

EXTENSION_MAP = {
    ".py": "python",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".js": "javascript",
    ".ts": "typescript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".sh": "shell",
}

def scan_directory(root_path):
    file_records = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)

            try:
                stat = os.stat(full_path)
                file_records.append({
                "path": full_path,
                "size": stat.st_size,
                "modified_at": stat.st_mtime,
                "language": detect_language(filename)
            })
            except OSError:
                # Skip files we can't access
                continue

    return file_records

def detect_language(filename):
    _, ext = os.path.splitext(filename)
    return EXTENSION_MAP.get(ext.lower(), "unknown")