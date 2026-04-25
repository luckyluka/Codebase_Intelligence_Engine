from scanner import save_structure
from dependency_graph import DependencyGraphBuilder


def main():
    print("Step 1: Scanning codebase...")
    save_structure()

    print("Step 2: Building dependency graph...")
    builder = DependencyGraphBuilder()
    graph = builder.save()

    print(f"Done. Built {len(graph['edges'])} edges")


if __name__ == "__main__":
    main()