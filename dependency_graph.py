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

    def _norm(self, p):
        return p.replace("./", "")

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

                imp_type = imp.get("type")
                target = imp.get("target")

                if not target:
                    continue

                if imp_type == "local_or_external":
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

                elif imp_type == "stdlib":
                    edges.append({
                        "from": src,
                        "to": target,
                        "type": "stdlib_dependency",
                        "resolution": "resolved"
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