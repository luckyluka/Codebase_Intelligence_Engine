import json
import hashlib


def function_hash(functions: list) -> str:
    """
    Hash ONLY semantic structure, not metadata like timestamps
    """
    normalized = []

    for f in functions:
        normalized.append({
            "name": f.get("name"),
            "args": f.get("args", []),
            "hash": f.get("hash")  # from extractor (best signal)
        })

    raw = json.dumps(normalized, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def file_hash(file_obj: dict) -> str:
    """
    Stable semantic fingerprint of a file
    """
    content = {
        "imports": file_obj.get("imports", []),
        "functions": [
            {
                "name": f.get("name"),
                "args": f.get("args", []),
                "hash": f.get("hash")
            }
            for f in file_obj.get("functions", [])
        ]
    }

    raw = json.dumps(content, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class DiffEngine:
    def __init__(self, prev_snapshot=None, curr_snapshot=None):
        self.prev = prev_snapshot or []
        self.curr = curr_snapshot or []

    def _index(self, snapshot):
        # 🔥 identity MUST be path only
        return {f["path"]: f for f in snapshot}

    def compute(self):
        prev_map = self._index(self.prev)
        curr_map = self._index(self.curr)

        added = []
        removed = []
        modified = []

        # -----------------------------
        # ADD / MODIFY
        # -----------------------------
        for path, curr_file in curr_map.items():
            if path not in prev_map:
                added.append(curr_file)
            else:
                prev_file = prev_map[path]

                if file_hash(prev_file) != file_hash(curr_file):
                    modified.append({
                        "path": path,
                        "prev": prev_file,
                        "curr": curr_file
                    })

        # -----------------------------
        # REMOVE
        # -----------------------------
        for path, prev_file in prev_map.items():
            if path not in curr_map:
                removed.append(prev_file)

        return {
            "added": added,
            "modified": modified,
            "removed": removed
        }