import json
from typing import Dict, List


class DiffEngine:
    def __init__(self, old_path="structure.json", new_data=None):
        self.old_path = old_path
        self.new_data = new_data or []

    def load_old(self):
        try:
            with open(self.old_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def index_functions(self, structure):
        """
        Build lookup:
        {
            "file.py::function_name": hash
        }
        """
        index = {}

        for file in structure:
            path = file["path"]

            for fn in file.get("functions", []):
                key = f"{path}::{fn['name']}"
                index[key] = fn.get("hash")

        return index

    def compute_diff(self):
        old = self.load_old()
        new = self.new_data

        old_index = self.index_functions(old)
        new_index = self.index_functions(new)

        added = []
        modified = []
        removed = []

        # NEW + MODIFIED
        for key, new_hash in new_index.items():
            if key not in old_index:
                added.append(key)
            elif old_index[key] != new_hash:
                modified.append(key)

        # REMOVED
        for key in old_index:
            if key not in new_index:
                removed.append(key)

        return {
            "added": added,
            "modified": modified,
            "removed": removed
        }


def run_diff(new_structure):
    engine = DiffEngine(new_data=new_structure)
    return engine.compute_diff()