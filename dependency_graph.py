import json


class DependencyGraphBuilder:
    def __init__(self, structure_path="structure.json"):
        self.structure_path = structure_path

        self.stdlib = {
            "os", "json", "ast", "sys", "math", "time", "re",
            "typing", "pathlib", "datetime"
        }

    def _resolve_local(self, target, files):
        expected = f"{target}.py"

        for f in files:
            if f.endswith(expected):
                return f
        return None

    def build(self):
        with open(self.structure_path, "r", encoding="utf-8") as f:
            structure = json.load(f)

        files = [f["path"].replace("./", "") for f in structure]

        edges = []

        for entry in structure:
            src = entry["path"].replace("./", "")
            imports = entry.get("imports", [])

            for imp in imports:

                if not isinstance(imp, dict):
                    continue

                target = imp.get("target")
                imp_type = imp.get("type")

                if not target:
                    continue

                # --------------------------------------------------
                # STD LIB CHECK (MUST BE FIRST)
                # --------------------------------------------------
                if target in self.stdlib:
                    edges.append({
                        "from": src,
                        "to": target,
                        "type": "stdlib_dependency",
                        "resolution": "resolved"
                    })
                    continue

                # --------------------------------------------------
                # LOCAL RESOLUTION
                # --------------------------------------------------
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

        return {"edges": self._deduplicate(edges)}

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