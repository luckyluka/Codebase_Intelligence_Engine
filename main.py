from scanner import save_structure
from dependency_graph import DependencyGraphBuilder
from diff_engine import DiffEngine
from impact_analyzer import ImpactAnalyzer
import json
import os


def load_snapshot(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def main():
    print("Step 0: Loading previous snapshot...")

    prev = load_snapshot("snapshot_prev.json")

    print("Step 1: Scanning codebase...")
    curr = save_structure("structure.json")

    print("Step 2: Building dependency graph...")
    builder = DependencyGraphBuilder()
    graph = builder.save()

    print("Step 3: Computing changes...")
    diff = DiffEngine(prev, curr).compute()

    print("Done computing diff.")
    print(f"Added: {len(diff['added'])}")
    print(f"Modified: {len(diff['modified'])}")
    print(f"Removed: {len(diff['removed'])}")

    print("Step 4: Computing impact analysis...")

    with open("dependency_graph.json", "r") as f:
        graph = json.load(f)

    analyzer = ImpactAnalyzer(graph)

    changed_files = [
        f["path"]
        for f in diff["modified"]
    ] + [
        f["path"]
        for f in diff["added"]
    ]

    impact = analyzer.compute(changed_files)

    print(f"Directly impacted files: {len(impact['direct'])}")
    print(f"Transitive impact scope: {len(impact['transitive'])}")

    print("Step 5: Saving new snapshot...")
    with open("snapshot_curr.json", "w") as f:
        json.dump(curr, f, indent=2)

    print("Step 6: Promoting curr → prev...")
    os.replace("snapshot_curr.json", "snapshot_prev.json")
    print("done")


if __name__ == "__main__":
    main()