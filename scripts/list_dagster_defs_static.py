import ast
from pathlib import Path


def extract_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        # Reconstruct dotted path
        parts = []
        while isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            parts.append(node.id)
            return ".".join(reversed(parts))
    if isinstance(node, ast.Call):
        # Handle calls like some_wrapper(asset_fn)
        if node.args:
            return extract_name(node.args[0])
    return ast.unparse(node) if hasattr(ast, "unparse") else str(node)


def list_defs(defs_py: Path) -> dict:
    tree = ast.parse(defs_py.read_text(encoding="utf-8"), filename=str(defs_py))
    results = {"assets": [], "jobs": [], "schedules": []}

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id == "defs" for t in node.targets):
                if isinstance(node.value, ast.Call):
                    call = node.value
                    func_name = getattr(call.func, "id", None) or getattr(call.func, "attr", None)
                    if func_name == "Definitions":
                        for kw in call.keywords:
                            if kw.arg in results and isinstance(kw.value, (ast.List, ast.Tuple)):
                                items = []
                                for elt in kw.value.elts:
                                    items.append(extract_name(elt))
                                results[kw.arg] = items
    return results


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    defs_path = repo_root / "packages" / "confradar" / "src" / "confradar" / "dagster" / "definitions.py"
    if not defs_path.exists():
        raise SystemExit(f"Definitions file not found: {defs_path}")
    data = list_defs(defs_path)
    print("Dagster Definitions (static parse):")
    for k in ("assets", "jobs", "schedules"):
        print(f"- {k}:")
        for name in data.get(k, []):
            print(f"  • {name}")
