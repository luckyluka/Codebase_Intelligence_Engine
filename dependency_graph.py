import json


class DependencyGraphBuilder:
    def __init__(self, structure_path="structure.json"):
        self.structure_path = structure_path

        self.stdlib = {
            "os", "json", "ast", "sys", "math", "time", "re",
            "typing", "pathlib", "datetime"
        }

    def _norm(self, path: str) -> str:
        return path.replace("./", "")

    def _resolve_local(self, target, files):
        """
        Resolve module -> file path
        scanner -> scanner.py
        """
        expected = f"{target}.py"
        for f in files:
            if f.endswith(expected):
                return f
        return None

    def build(self):
        with open(self.structure_path, "r", encoding="utf-8") as f:
            structure = json.load(f)

        files = [self._norm(f["path"]) for f in structure]

        edges = []

        for entry in structure:
            src = self._norm(entry["path"])
            imports = entry.get("imports", [])

            for imp in imports:
                if not isinstance(imp, dict):
                    continue

                target = imp.get("target")
                imp_type = imp.get("type")

                if not target:
                    continue

                # ---------------------------
                # STDLIB
                # ---------------------------
                if target in self.stdlib or imp_type == "stdlib":
                    edges.append({
                        "from": src,
                        "to": target,
                        "type": "stdlib_dependency",
                        "resolution": "resolved"
                    })

                # ---------------------------
                # LOCAL / EXTERNAL
                # ---------------------------
                elif imp_type == "local_or_external":
                    local = self._resolve_local(target, files)

                    if local:
                        edges.append({
                            "from": src,
                            "to": local,
                            "type": "local_dependency",
                            "resolution": "resolved"
                        })
                    else:
                        edges.append({
                            "from": src,
                            "to": target,
                            "type": "external_dependency",
                            "resolution": "unresolved"
                        })

        edges = self._deduplicate(edges)

        return {
            "edges": edges,
            "reverse_index": self._build_reverse_index(edges)
        }

    def _build_reverse_index(self, edges):
        """
        to -> list of dependents
        required for impact analysis
        """
        rev = {}

        for e in edges:
            to = e["to"]
            frm = e["from"]

            rev.setdefault(to, set()).add(frm)

        # convert sets to lists for JSON safety
        return {k: list(v) for k, v in rev.items()}

    def _deduplicate(self, edges):
        seen = set()
        out = []

        for e in edges:
            key = (e["from"], e["to"], e["type"])
            if key in seen:
                continue
            seen.add(key)
            out.append(e)

        return out

    def save(self, output_path="dependency_graph.json"):
        graph = self.build()

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=2)

        return graph


if __name__ == "__main__":
    builder = DependencyGraphBuilder()
    result = builder.save()
    print("Edges:", len(result["edges"]))