from scanner import save_structure
from dependency_graph import DependencyGraphBuilder
from diff_engine import DiffEngine
from state_manager import StateManager


def main():
    state = StateManager()

    print("Step 0: Loading previous snapshot...")
    old_structure = state.load_prev()

    print("Step 1: Scanning codebase...")
    new_structure = save_structure()

    print("Step 2: Building dependency graph...")
    builder = DependencyGraphBuilder()
    graph = builder.save()

    print("Step 3: Computing changes...")

    diff_engine = DiffEngine(new_data=new_structure)
    diff_engine.old_path = state.prev_path  # important
    diff = diff_engine.compute_diff()

    print(f"Done. Built {len(graph['edges'])} edges")
    print(f"Added: {len(diff['added'])}")
    print(f"Modified: {len(diff['modified'])}")
    print(f"Removed: {len(diff['removed'])}")

    print("Step 4: Saving new snapshot...")
    state.save_curr(new_structure)

    print("Step 5: Promoting curr → prev...")
    state.promote_curr_to_prev()


if __name__ == "__main__":
    main()