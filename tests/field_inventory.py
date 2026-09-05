"""Generate the field inventory and compare immutable structural baselines."""
import csv
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fields(schema):
    result = {}
    def walk(node, path, required=False):
        if not isinstance(node, dict):
            return
        if "$ref" in node:
            target = schema
            for part in node["$ref"].removeprefix("#/").split("/"):
                target = target[part]
            node = {**target, **{k:v for k,v in node.items() if k != "$ref"}}
        if path and not path.endswith(".*") and not path.endswith("[]"):
            result[path] = {
                "type": node.get("type", "union" if "oneOf" in node else "constraint"),
                "required": required,
                "default": node.get("default", "not supplied by schema"),
                "description": node.get("description", ""),
            }
        for name, value in node.get("properties", {}).items():
            walk(value, f"{path}.{name}".strip("."), name in node.get("required", []))
        walk(node.get("additionalProperties"), path + ".*")
        walk(node.get("items"), path + "[]")
        for pattern, value in node.get("patternProperties", {}).items():
            walk(value, path + ".<" + pattern + ">")
    walk(schema, "")
    return result


def render():
    schema = json.loads((ROOT / "schema/bmopf/0.2.0/bmopf.schema.json").read_text())
    current = fields(schema)
    baselines = json.loads((ROOT / "contracts/field-baselines.json").read_text())
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(["field", "type", "required", "default", "historical_draft", "legacy_0.1", "proposal_baseline", "semantics_and_units", "implementation_evidence"])
    for path, value in sorted(current.items()):
        writer.writerow([path, value["type"], value["required"], value["default"],
            *[path in baselines[name]["fields"] for name in ("historical_draft", "legacy_0.1", "proposal_baseline")],
            value["description"], "docs/conformance.md; parsing/preservation do not imply solver support"])
    return out.getvalue()


if __name__ == "__main__":
    path = ROOT / "docs/fields.csv"
    text = render()
    if "--check" in sys.argv:
        if path.read_text() != text:
            sys.exit("docs/fields.csv differs; run python3 tests/field_inventory.py")
    else:
        path.write_text(text)
