"""Cross-field BMOPF checks that JSON Schema cannot express.

The checks operate on decoded data and never retrieve URLs or execute profiles.
Findings use JSON-pointer locations and stable codes. Schema validation remains
necessary before computational capability checks.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from collections.abc import Iterator


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str


def escape(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def records(doc: dict, kind: str) -> Iterator[tuple[str, dict]]:
    table = doc.get(kind, {})
    if isinstance(table, dict):
        for name, record in table.items():
            if isinstance(record, dict):
                yield f"/{kind}/{escape(name)}", record


def validate(doc: dict) -> list[Finding]:
    findings: list[Finding] = []

    def fail(code, path, message):
        findings.append(Finding(code, path, message))

    meta = doc.get("meta", {})
    identity = meta.get("$schema", "")
    version = meta.get("schema_version")
    match = re.search(r"/(0\.[12]\.0)/", identity)
    inferred = match[1] if match else "0.1.0" if "bmopf-report" in identity or "draft_bmopf_schema" in identity else None
    if inferred is not None and version is not None and inferred != version:
        fail("BMOPF.VERSION", "/meta/schema_version", "Schema identity and schema_version disagree")

    conventions = doc.get("terminal_conventions")
    if conventions is not None:
        seen = set()
        for role in ("phase", "neutral", "earth"):
            labels = conventions.get(role, [])
            if len(set(labels)) != len(labels) or seen.intersection(labels):
                fail("BMOPF.TERMINAL_ROLE", f"/terminal_conventions/{role}", "Role lists must be unique and disjoint")
            seen.update(labels)

    def phases(names):
        if conventions is not None:
            nonphase = set(conventions.get("neutral", []) + conventions.get("earth", []))
        else:
            nonphase = {"n", "N"}
            if set(names) == {"1", "2", "3", "4"}:
                nonphase.add("4")
        return [name for name in names if name not in nonphase]

    def dimension(record, key, expected, path):
        if key in record and isinstance(record[key], list):
            allowed = expected if isinstance(expected, tuple) else (expected,)
            if len(record[key]) not in allowed:
                fail("BMOPF.DIMENSION", f"{path}/{key}", f"Expected length {allowed}, found {len(record[key])}")

    buses = doc.get("bus", {})

    def terminal_map(record, bus_key, map_key, path):
        if bus_key not in record:
            return
        bus = buses.get(record[bus_key])
        if bus is None:
            fail("BMOPF.REFERENCE", f"{path}/{bus_key}", "Bus does not exist")
            return
        names = record.get(map_key, [])
        for name in names:
            if name != "g" and name not in bus.get("terminal_names", []):
                fail("BMOPF.REFERENCE", f"{path}/{map_key}", f"Terminal {name!r} does not exist on the bus")

    def matrices(record, size, path):
        for key in record:
            cell = re.fullmatch(r"(?:R_series|X_series|G_shunt|B_shunt|G_from|B_from|G_to|B_to|G|B)_(\d+)_(\d+)", key)
            if cell and not (1 <= int(cell[1]) <= size and 1 <= int(cell[2]) <= size):
                fail("BMOPF.MATRIX", f"{path}/{key}", f"Matrix index exceeds conductor dimension {size}")

    for path, bus in records(doc, "bus"):
        names = bus.get("terminal_names", [])
        if not names or len(set(names)) != len(names) or "g" in names:
            fail("BMOPF.TERMINAL", path + "/terminal_names", "Bus terminals must be nonempty, unique and exclude implicit ground g")
        if not set(bus.get("perfectly_grounded_terminals", [])).issubset(names):
            fail("BMOPF.REFERENCE", path + "/perfectly_grounded_terminals", "Grounded terminals must belong to the bus")
        nphase = len(phases(names))
        for key in ("v_min", "v_max", "vpn_min", "vpn_max"):
            dimension(bus, key, nphase, path)
        for key in ("vpp_min", "vpp_max"):
            dimension(bus, key, nphase * (nphase - 1) // 2, path)
        for lo, hi in (("v_min", "v_max"), ("vpn_min", "vpn_max"), ("vpp_min", "vpp_max")):
            if lo in bus and hi in bus and any(a > b for a, b in zip(bus[lo], bus[hi])):
                fail("BMOPF.BOUNDS", path, f"{lo} exceeds {hi}")

    for kind in ("line", "switch"):
        for path, line in records(doc, kind):
            for side in ("from", "to"):
                terminal_map(line, f"bus_{side}", f"terminal_map_{side}", path)
            n = len(line.get("terminal_map_from", []))
            dimension(line, "terminal_map_to", n, path)
            matrices(line, n, path)
            dimension(line, "i_max", n, path)
            dimension(line, "s_max", len(phases(line.get("terminal_map_from", []))), path)
            if "linecode" in line:
                code = doc.get("linecode", {}).get(line["linecode"])
                if code is None:
                    fail("BMOPF.REFERENCE", path + "/linecode", "Linecode does not exist")
                else:
                    matrices(code, n, path + "/linecode")
                    dimension(code, "i_max", n, path + "/linecode")
                    dimension(code, "s_max", len(phases(line.get("terminal_map_from", []))), path + "/linecode")

    for kind in ("load", "generator", "voltage_source", "ibr", "shunt", "capacitor", "grounding"):
        for path, record in records(doc, kind):
            terminal_map(record, "bus", "terminal_map", path)
            names = record.get("terminal_map", [])
            nt = len(names)
            np = len(phases(names))
            if kind == "load":
                configuration = record.get("configuration")
                np = 1 if configuration == "SINGLE_PHASE" else max(0, nt - 1) if configuration == "WYE" else nt * (nt - 1) // 2
                for key in ("p_nom", "q_nom", "v_nom", "alpha_p", "alpha_i", "alpha_z", "beta_p", "beta_i", "beta_z", "gamma_p", "gamma_q"):
                    dimension(record, key, np, path)
            elif kind == "voltage_source":
                for key in ("v_magnitude", "v_angle"):
                    dimension(record, key, nt, path)
                for key in ("p_min", "p_max", "cost"):
                    dimension(record, key, np, path)
            elif kind in ("generator", "ibr"):
                for key in ("p_min", "p_max", "q_min", "q_max", "s_max", "cost"):
                    dimension(record, key, np, path)
                dimension(record, "i_max", (np, nt) if kind == "generator" else nt, path)
            matrices(record, nt, path)
            for field, table in (("control_profile", "control_profile"), ("dc_bus", "dc_bus")):
                if field in record and record[field] not in doc.get(table, {}):
                    fail("BMOPF.REFERENCE", path + "/" + field, f"Referenced {table} does not exist")

    def check_transformer(record, path):
        if "no_load_shunt" in record:
            shunt = record["no_load_shunt"]
            count = len(record["windings"]) if "windings" in record else 3 if "/center_tap/" in path else 2
            index = shunt.get("winding") if isinstance(shunt, dict) else None
            if not isinstance(index, int) or isinstance(index, bool) or not 1 <= index <= count:
                fail("BMOPF.REFERENCE", path + "/no_load_shunt/winding", "No-load shunt winding does not exist")
            if "g_no_load" in record or "b_no_load" in record:
                fail("BMOPF.AMBIGUOUS", path + "/no_load_shunt", "Use one no-load admittance representation")
        for side in ("from", "to"):
            terminal_map(record, f"bus_{side}", f"terminal_map_{side}", path)
        for root in ("tap_ratio", "tap"):
            values = [record.get(root + suffix) for suffix in ("_min", "_max", "")]
            size = 2 if "/open_delta_regulator/" in path else 1
            for suffix in ("_min", "_max", ""):
                dimension(record, root + suffix, size, path)
            for index in range(size):
                lo, hi, value = [v[index] if isinstance(v, list) and index < len(v) else v if not isinstance(v, list) else None for v in values]
                if lo is not None and hi is not None and lo > hi:
                    fail("BMOPF.BOUNDS", path, "Minimum tap exceeds maximum tap")
                if value is not None and (value <= 0 or (lo is not None and value < lo) or (hi is not None and value > hi)):
                    fail("BMOPF.BOUNDS", path + "/" + root, "Tap must be positive and lie inside stated bounds")
        for index, winding in enumerate(record.get("windings", [])):
            terminal_map(winding, "bus", "terminal_map", f"{path}/windings/{index}")
            check_transformer(winding, f"{path}/windings/{index}")

    for subtype, table in doc.get("transformer", {}).items():
        for name, record in table.items():
            check_transformer(record, f"/transformer/{escape(subtype)}/{escape(name)}")
    def numeric(value):
        return isinstance(value, (int, float)) and not isinstance(value, bool) or isinstance(value, list) and bool(value) and all(numeric(v) for v in value)

    def walk(record, path):
        if isinstance(record, list):
            for index, item in enumerate(record):
                walk(item, f"{path}/{index}")
            return
        if not isinstance(record, dict):
            return
        for field in ("control_profile", "line_geometry", "wire_data"):
            if isinstance(record.get(field), str) and record[field] not in doc.get(field, {}):
                fail("BMOPF.REFERENCE", path + "/" + field, "Referenced record does not exist")
        for bus_field, map_field in (("dc_bus", "terminal_map"), ("dc_bus_from", "terminal_map_from"), ("dc_bus_to", "terminal_map_to")):
            if bus_field in record:
                bus = doc.get("dc_bus", {}).get(record[bus_field])
                names = record.get("dc_terminal_map", record.get(map_field, [record["terminal"]] if "terminal" in record else []))
                if bus is None or any(n not in bus.get("terminal_names", []) for n in names):
                    fail("BMOPF.REFERENCE", path + "/" + bus_field, "DC bus or terminal does not exist")
        if path.startswith("/dc_branch/") and "dc_bus_from" in record:
            for field in ("terminal_map_to", "r", "i_max"):
                dimension(record, field, len(record.get("terminal_map_from", [])), path)
        if path.startswith("/dc_bus/") and "terminal_names" in record:
            names = record["terminal_names"]
            if len(names) != len(set(names)) or not set(record.get("perfectly_grounded_terminals", [])).issubset(names) or not set(record.get("pole", {})).issubset(names):
                fail("BMOPF.TERMINAL", path, "DC terminal identities are inconsistent")
            for field in ("v_dc_nom", "v_dc_min", "v_dc_max"):
                dimension(record, field, len(names), path)
            if any(a > b for a,b in zip(record.get("v_dc_min", []), record.get("v_dc_max", []))):
                fail("BMOPF.BOUNDS", path, "Minimum DC voltage exceeds maximum")
        for field, profile in record.get("time_series", {}).items():
            if not numeric(record.get(field)):
                fail("BMOPF.PROFILE", path + "/time_series/" + escape(field), "Profile requires a stated numeric field")
            if profile not in doc.get("time_series", {}):
                fail("BMOPF.REFERENCE", path + "/time_series/" + escape(field), "Time profile does not exist")
        if path.startswith("/time_series/") and "values" in record:
            dimension(record, "time", len(record["values"]), path)
            if any(a >= b for a,b in zip(record.get("time", []), record.get("time", [])[1:])):
                fail("BMOPF.PROFILE", path + "/time", "Profile time must be strictly increasing")
        if "windings" in record and "x_sc" in record:
            count = len(record["windings"])
            expected = {f"{i}_{j}" for i in range(1,count+1) for j in range(i+1,count+1)}
            if set(record["x_sc"]) != expected:
                fail("BMOPF.MATRIX", path + "/x_sc", "Short-circuit table must state every ordered winding pair")
        for field, item in record.items():
            if field not in ("meta", "extras", "provenance", "time_series"):
                walk(item, path + "/" + escape(field))

    for kind, table in doc.items():
        if kind not in ("meta", "extras", "terminal_conventions"):
            walk(table, "/" + escape(kind))
    return findings
