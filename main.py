import os
from scanner import save_structure
from dependency_graph import DependencyGraphBuilder
from diff_engine import DiffEngine


def main():
    print("Step 0: Loading previous snapshot...")

    old_path = "structure.json"

    if os.path.exists(old_path):
        import json
        with open(old_path, "r", encoding="utf-8") as f:
            old_structure = json.load(f)
    else:
        old_structure = []

    print("Step 1: Scanning codebase...")
    new_structure = save_structure()

    print("Step 2: Building dependency graph...")
    builder = DependencyGraphBuilder()
    graph = builder.save()

    print("Step 3: Computing changes...")

    engine = DiffEngine(new_data=new_structure)
    engine.old_path = old_path  # explicitly reuse same file
    diff = engine.compute_diff()

    print(f"Done. Built {len(graph['edges'])} edges")
    print(f"Added: {len(diff['added'])}")
    print(f"Modified: {len(diff['modified'])}")
    print(f"Removed: {len(diff['removed'])}")


if __name__ == "__main__":
    main()