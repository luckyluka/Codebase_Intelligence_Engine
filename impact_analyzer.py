class ImpactAnalyzer:
    def __init__(self, graph):
        self.graph = graph
        self.reverse_index = graph.get("reverse_index", {})

    def compute(self, changed_files):
        direct = set()
        visited = set()

        # ------------------------
        # direct impact
        # ------------------------
        for file in changed_files:
            for dep in self.reverse_index.get(file, []):
                direct.add(dep)

        # ------------------------
        # transitive closure (BFS)
        # ------------------------
        stack = list(direct)

        while stack:
            node = stack.pop()

            if node in visited:
                continue

            visited.add(node)

            for parent in self.reverse_index.get(node, []):
                if parent not in visited:
                    stack.append(parent)

        return {
            "direct": sorted(direct),
            "transitive": sorted(visited)
        }