from collections import defaultdict


class ImpactAnalyzer:
    def __init__(self, graph):
        self.graph = graph["edges"]

        self.reverse_map = defaultdict(list)

        for edge in self.graph:
            src = self._norm(edge["from"])
            dst = self._norm(edge["to"])
            self.reverse_map[dst].append(src)

    def _norm(self, p):
        return p.replace("./", "")

    def get_direct_impact(self, changed_files):
        changed_files = [self._norm(f) for f in changed_files]

        impacted = set()

        for f in changed_files:
            for dep in self.reverse_map.get(f, []):
                impacted.add(dep)

        return list(impacted)

    def get_transitive_impact(self, changed_files, depth=3):
        changed_files = [self._norm(f) for f in changed_files]

        visited = set()
        frontier = set(changed_files)

        for _ in range(depth):
            next_frontier = set()

            for node in frontier:
                for dep in self.reverse_map.get(node, []):
                    if dep not in visited:
                        next_frontier.add(dep)

            visited.update(frontier)
            frontier = next_frontier

        return list(visited - set(changed_files))