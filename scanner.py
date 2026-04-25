import os


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
                    "modified_at": stat.st_mtime
                })
            except OSError:
                # Skip files we can't access
                continue

    return file_records