"""Semantic rejection tests and immutable historical findings."""
import copy
import hashlib
import json
import unittest
from pathlib import Path
from semantics import validate

ROOT = Path(__file__).resolve().parent.parent


class SemanticContract(unittest.TestCase):
    def setUp(self):
        self.case = json.loads((ROOT / "examples/0.2.0/worked_feeder.json").read_text())

    def test_worked_example(self):
        self.assertEqual(validate(self.case), [])

    def test_role_lists_are_disjoint(self):
        self.case["terminal_conventions"]["earth"] = ["n"]
        self.assertIn("BMOPF.TERMINAL_ROLE", {f.code for f in validate(self.case)})

    def test_phase_bounds_do_not_include_neutral(self):
        self.case["bus"]["load"]["v_min"].append(0)
        self.assertIn("BMOPF.DIMENSION", {f.code for f in validate(self.case)})

    def test_terminal_order_controls_dimensions(self):
        self.case["line"]["feeder"]["terminal_map_to"].pop()
        self.assertIn("BMOPF.DIMENSION", {f.code for f in validate(self.case)})

    def test_references_and_matrix_dimensions(self):
        self.case["line"]["feeder"]["bus_to"] = "absent"
        self.case["linecode"]["cable"]["R_series_5_5"] = 0.01
        self.assertTrue({"BMOPF.REFERENCE", "BMOPF.MATRIX"}.issubset({f.code for f in validate(self.case)}))

    def test_versions_cannot_disagree(self):
        self.case["meta"]["schema_version"] = "0.1.0"
        self.assertIn("BMOPF.VERSION", {f.code for f in validate(self.case)})

    def test_metadata_is_not_interpreted_as_equipment(self):
        self.case["meta"]["provenance"] = {"bus": "missing", "tap_ratio_min": 2, "tap_ratio_max": 1}
        self.case["extras"] = {"arbitrary": {"terminal_map": ["absent"]}}
        self.assertEqual(validate(self.case), [])

    def test_tap_bounds(self):
        self.case["transformer"] = {"single_phase_autotransformer": {"r": {
            "bus_from": "source", "bus_to": "load", "terminal_map_from": ["a", "n"],
            "terminal_map_to": ["a", "n"], "tap_ratio": 1.2, "tap_ratio_min": 0.9, "tap_ratio_max": 1.1,
        }}}
        self.assertIn("BMOPF.BOUNDS", {f.code for f in validate(self.case)})

    def test_parallel_conductors_may_share_a_bus_terminal(self):
        self.case["line"]["feeder"]["terminal_map_from"] = ["a", "a", "a", "n"]
        self.assertEqual(validate(self.case), [])

    def test_dc_maps_and_profiles(self):
        self.case["dc_bus"] = {"d": {"terminal_names": ["p", "r"], "v_dc_min": [0]}}
        self.case["dc_load"] = {"load": {"dc_bus": "d", "terminal_map": ["absent", "r"], "p": 5}}
        self.case["time_series"] = {"bad": {"values": [1, 2], "time": [1, 0]}}
        self.case["line"]["feeder"]["time_series"] = {"length": "missing", "bus_from": "bad"}
        codes = {f.code for f in validate(self.case)}
        self.assertTrue({"BMOPF.DIMENSION", "BMOPF.REFERENCE", "BMOPF.PROFILE"}.issubset(codes))

    def test_winding_pairs_and_geometry_references(self):
        self.case["transformer"] = {"n_winding": {"t": {"windings": [{}, {}, {}], "x_sc": {"2_1": 1}}}}
        self.case["line_geometry"] = {"g": {"conductors": [{"wire_data": "absent"}]}}
        codes = {f.code for f in validate(self.case)}
        self.assertTrue({"BMOPF.MATRIX", "BMOPF.REFERENCE"}.issubset(codes))

    def test_no_load_shunt_has_a_physical_winding(self):
        self.case["transformer"] = {"single_phase": {"t": {"no_load_shunt": {"winding": 3, "g": 0.1, "b": -0.2}}}}
        self.assertIn("BMOPF.REFERENCE", {f.code for f in validate(self.case)})
        t = self.case["transformer"]["single_phase"]["t"]
        t["no_load_shunt"]["winding"] = 2
        self.assertEqual(validate(self.case), [])
        t["g_no_load"] = 0
        self.assertIn("BMOPF.AMBIGUOUS", {f.code for f in validate(self.case)})

    def test_historical_examples_keep_their_recorded_findings(self):
        contract = json.loads((ROOT / "contracts/historical.json").read_text())
        for name, expected in contract.items():
            data = (ROOT / name).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), expected["sha256"], name)
            self.assertEqual([[f.code, f.path] for f in validate(json.loads(data))], expected["findings"], name)


if __name__ == "__main__":
    unittest.main()
