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



def implementation(path):
    family = path.split(".", 1)[0]
    spec = {"meta": "metadata", "name": "data-format", "extras": "metadata", "terminal_conventions": "notation", "voltage_source": "source", "linecode": "line"}.get(family, family)
    accepted = {"bus", "line", "load", "generator", "source", "shunt", "capacitor", "switch", "transformer", "metadata", "notation", "data-format"}
    reference = f"spec/{spec}.md" if spec in accepted else "proposals/bmopf-0.2.0.md#other-proposed-equipment-and-controls"
    reader = "powerio-dist/src/bmopf/read.rs"
    writer = "powerio-dist/src/bmopf/write.rs"
    metadata = family in {"meta", "extras", "terminal_conventions", "name"}
    retained = family in {"dc_bus", "dc_branch", "dc_grounding", "dc_load", "dc_source", "time_series", "wire_data", "line_geometry"}
    if metadata:
        read = "Dataset name/frequency typed; metadata and role declarations retained as complete JSON"
        compute = "Metadata only; role declarations affect conductor ordering; no executable instructions"
    elif retained:
        read = "Preserved as untyped named JSON records in the multiconductor model and generation-2 IR"
        compute = "No PowerIO snapshot equation compilation for this table; consumer must implement it explicitly"
    else:
        read = "Typed multiconductor component; non-typed source fields retained in component extras"
        compute = "PowerIO stores data and builds declared calculation instances; it does not solve OPF"
    if family in {"line", "linecode", "shunt", "switch"}:
        compute = "Passive admittance compilation with conductor ordering; switches use their stated closed/open state"
    if family == "transformer":
        compute = "PowerIO passive matrix accepts only fixed ideal grounded-WYE pairs; other required transformer physics rejects before calculation"
    if family in {"ibr", "control_profile"}:
        compute = "Typed preservation; solving control laws, filter equations and coupled DC physics requires a capable consumer"
    if ".no_load_shunt" in path:
        read = "Complete explicit coil-shunt object retained in transformer extras and generation-2 IR"
        compute = "PowerIO passive matrix rejects nonzero core shunts; BMOPFTools materializes an equivalent bus shunt without moving it across leakage"
    if family == "bus" and path.endswith((".v_min", ".v_max")):
        read = "Unequal phase bounds retained as ordered vectors; a scalar update explicitly overrides the vector"
        compute = "Balanced lowering rejects unequal phase limits; ABI 7 and Julia expose the ordered phase vectors"
    preservation = "Same-format unmodified module emits original bytes; IR omits source bytes and retains typed values plus JSON metadata"
    if family in {"wire_data", "line_geometry"}:
        emission = "Named JSON retained under extras when no typed target representation exists, with a relocation diagnostic; geometry is not silently compiled"
    elif retained or family in {"ibr", "control_profile"}:
        emission = "Proposal top-level table when declared; explicit 0.1.0 relocates unsupported tables under extras and reports the move"
    elif family == "transformer":
        emission = "Proposal named fields; 0.1.0 relocates taps/neutrals/core fields and complete regulator/n-winding records into extras.transformer"
    elif metadata:
        emission = "Preserve legitimate metadata; producer sets selected schema identity, immutable retrieval URL, status and digest"
    else:
        emission = "Re-encode supported typed fields in declared SI units; report fields or projections the target cannot represent"
    if ".no_load_shunt" in path:
        emission = "Proposal explicit per-coil shunt; 0.1.0 relocation; winding-2 shunts convert to DSS/PMD exciting-branch parameters, other locations report unsupported projection"
    validation = "JSON Schema type/shape/requiredness; tests/semantics.py and PowerIO bmopf/validate.rs check cross-field relations"
    if metadata:
        validation = "Schema metadata shape and consistent schema identifiers; free-form extras/provenance do not undergo equipment traversal"
    evidence = "PowerIO powerio-dist/tests/bmopf.rs: schema_fields_survive_a_round_trip_without_wrong_warnings; every_dist_fixture_emits_valid_bmopf"
    if ".no_load_shunt" in path:
        evidence = "PowerIO no_load_shunt_preserves_winding_units_and_tap_after_conversion; evals/validation/validate_bmopf_core_shunts.py; BMOPFTools test/powerio_v09_tests.jl"
    elif family == "bus" and path.endswith((".v_min", ".v_max")):
        evidence = "PowerIO nonuniform_phase_bounds_survive_value_serialization_and_emission; facade IR tests; C ABI/Julia phase-view tests"
    elif family in {"meta", "extras"}:
        evidence = "PowerIO proposal_provenance_is_pinned_and_preserves_existing_keys; tests/test_semantics.py metadata/version cases"
    elif retained:
        evidence = "Structural example_features.json; family preservation tests in PowerIO bmopf.rs; no field-specific numerical certification"
    elif family == "transformer":
        evidence = "PowerIO bmopf.rs transformer/regulator/n_winding mutation and conversion regressions; BMOPFTools test/powerio_v09_tests.jl; numerical support remains formulation-specific"
    return [reference, read, preservation, emission, compute, validation, evidence, reader, writer]

def render():
    schema = json.loads((ROOT / "schema/bmopf/0.2.0/bmopf.schema.json").read_text())
    current = fields(schema)
    baselines = json.loads((ROOT / "contracts/field-baselines.json").read_text())
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(["field", "type", "required", "default", "historical_draft", "legacy_0.1", "proposal_baseline", "semantics_and_units", "specification", "powerio_reader", "preservation_and_ir", "explicit_writer", "computational_support", "validation", "test_evidence", "reader_source", "writer_source"])
    for path, value in sorted(current.items()):
        writer.writerow([path, value["type"], value["required"], value["default"],
            *[path in baselines[name]["fields"] for name in ("historical_draft", "legacy_0.1", "proposal_baseline")],
            value["description"], *implementation(path)])
    return out.getvalue()


if __name__ == "__main__":
    path = ROOT / "docs/fields.csv"
    text = render()
    if "--check" in sys.argv:
        if path.read_text() != text:
            sys.exit("docs/fields.csv differs; run python3 tests/field_inventory.py")
    else:
        path.write_text(text)
