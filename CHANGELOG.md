# Changelog

Notable changes to the BMOPF JSON Schema. The format is loosely based on
[Keep a Changelog](https://keepachangelog.com).

## 0.2.0 (proposed, not ratified)

A proposal under the Task Force review tier of the specification's contributing
guide. It adds element classes and settles four questions the 0.1.0 text leaves
open. Nothing here is accepted material until the Task Force ratifies it.

Compatibility is checked against named examples and the field inventory in
[the conformance packet](docs/conformance.md). The historical ENWL example
still passes structural validation; semantic validation reports its existing
reference to an undeclared grounded terminal. The proposal deliberately rejects
ambiguous line impedance sources, contradictory version declarations, invalid
array dimensions, unresolved electrical references, and inconsistent bounds.
A structural acceptance result alone does not establish numerical equivalence.

### Integration corrections

- Use `energy_cost_rate` in $/kWh, following the coordinated source/objective
  proposal. Keep `cost` as a deprecated compatible spelling. Source, generator and IBR prices follow phase order.

- Preserve n-winding ratings, tap ratios and winding-neutral impedances with
  explicit winding fields; keep per-winding current limits and tap bounds.
- Distinguish an absent internal neutral branch from an explicitly zero
  grounding impedance. This preserves existing terminal-map-only models and
  makes OpenDSS open-neutral conversion unambiguous.
- Require two entries in each open-delta regulator tap array.
- Add semantic checks for versions, roles, dimensions, references and bounds.
- Separate canonical schema identity from immutable proposal retrieval and
  preserve both metadata extension locations, including `meta.provenance`.

### Added, restored from the archived draft

These classes were in the draft schema of
`distribution-system-opt/bmopf-resources` until 2026-07-21, when commits
`afda547` ("remove regulators, taps, ibrs, dc") and `9c9b26f` ("remove time
series") removed them. They are restored from `2e0b1cb`, the last commit holding
the complete set, with their descriptions rewritten against the accepted 0.1.0
conventions.

- `ibr`: inverter-based resources. Photovoltaic, battery, generic, and static
  compensator prime movers; single-phase, three-leg and four-leg topologies;
  per-phase apparent power, active power and reactive power limits; per
  conductor current limits; converter filter impedance; grid-forming operation;
  a reference to a `control_profile`; DC-side coupling to a `dc_bus` with a
  constant power, voltage master, or droop control mode. The objective page of
  the specification already sums over IBRs, so this is the element that page
  refers to.
- `control_profile`: reusable Volt-VAr, Volt-Watt and constant power factor
  control laws, referenced by an IBR the way a line references a linecode.
- `wire_data`: conductor and cable construction data with no geometry. Bare
  overhead round wire, concentric-neutral cable, and tape-shield cable.
- `line_geometry`: cross-section assemblies placing `wire_data` types at
  coordinates, each carrying one circuit terminal, compiled into a linecode.
  Resolves the dangling `line_geometry` reference in the specification's
  metadata page.
- `dc_bus`, `dc_branch`, `dc_grounding`, `dc_load`, `dc_source`: DC networks.
  Signed line-to-ground voltages with no angle, monopole and bipole nodes,
  per-conductor branch resistance, earthing perfectly or through impedance.
- `time_series`: named multiplicative profiles.
- `transformer.n_winding`: the general n-winding transformer as an ordered
  winding list with pairwise short-circuit reactances, winding 1 the reference.
- `transformer.single_phase_autotransformer` and
  `transformer.open_delta_regulator`: step-voltage regulators, with a bounded
  `tap_ratio` that is a free variable of the optimisation when its bounds
  differ and fixed otherwise, and ANSI type A or B connection.
- `tap_ratio`, `tap_ratio_min`, `tap_ratio_max`, `r_neutral_from`,
  `x_neutral_from`, `r_neutral_to`, `x_neutral_to`, `g_no_load`, `b_no_load` on
  the two-winding transformer subtypes. A two-winding `tap_ratio` is a
  multiplier on the nameplate turns ratio `v_nom_from / v_nom_to`, since that
  subtype has a nameplate ratio to multiply; a regulator's `tap_ratio` is a
  regulation ratio, since it has none.

### Added, new in this proposal

- `voltage_source.cost`, `voltage_source.p_min`, `voltage_source.p_max` and
  `ibr.cost`. The specification's objective sums a per-phase `cost` array over
  "generators, the voltage source, IBRs", but 0.1.0 defines `cost` only on
  `generator`, so two of the three summands had no field to read.
- `terminal_conventions.earth`, for a dedicated earth-wire terminal. The ground
  reference itself stays implicit.
- `meta.schema_version`, a constant equal to the version of the schema
  document. `meta.$schema` names the document, `meta.schema_version` pins its
  version, and `meta.version` stays the dataset's own version.
- A `time_series` reference map on every element that carries a numeric field,
  mapping a field name of that element to a profile id.
- `linecode.line_geometry` and `linecode.derivation`, recording which geometry a
  linecode was compiled from and by which method, earth model, frequency and
  temperature.

### Settled

- **Array dimensions.** Every array field states its own length rule. A bus
  voltage bound array is per phase terminal in `terminal_names` order and
  carries no entry for the neutral, which bounds through `vn_max`; the 0.1.0
  schema described these as "one entry per bus terminal", which contradicts the
  specification's bus page and the published `example_ieee13.json`. Phase-pair
  bounds are stated in the pair order (1,2), (2,3), (3,1). Load arrays are per
  sub-load, which for a delta load is the phase-pair count and not the phase
  count. Generator `i_max` is per phase with an optional trailing neutral-return
  entry.
- **Conductor ordering.** Position i of an element's own `terminal_map` fixes
  entry i of every per-terminal array and index i of every matrix key of that
  element. A linecode's ordering is the `terminal_map_from` ordering of every
  line that references it, so its conductor count is fixed and every
  referencing line states a terminal map of that width. A line geometry's
  ordering is its `conductors` order, and each conductor's `terminal` names what
  that row carries.
- **The transformer current limit.** `i_max_from` and `i_max_to` bound the
  winding current of their own side, in that side's own amperes, never referred
  through the turns ratio, with one entry per name in that side's terminal map.
  Position k bounds winding conductor k, which for a WYE winding is the
  conductor between bus terminal k and the winding and for a DELTA winding is
  coil k, which is not the terminal conductor current. For `center_tap` the
  entry against the centre terminal bounds the centre-tap current. The 0.1.0
  material called the same fields "per-conductor" in the data model table and
  "per-winding, per conductor" in the constraint, with no length stated.
- **Ideal equipment equations.** A new `$defs/ideal_equipment` block states, as
  equations, the ideal two-winding and n-winding transformer, the ideal
  autotransformer regulator of each ANSI type, the ideal closed and open switch,
  the ideal voltage source, and ideal DC grounding. A document declares ideal
  equipment by omitting its impedance fields, which read as zero.
- **Strict rejection.** Every object rejects unknown fields, and the matrix
  element names are the only pattern-matched keys. `control_profile` and
  `time_series`, which the archived draft left open, are strict too. The
  top-level `extras` object is the one free-form place, and its description
  states that a reader ignoring it reads a different network. `tests/rejected/`
  holds one document per rejection rule.

### Fixed

- A line's impedance source exclusion. 0.1.0 states the `oneOf` exclusion on one
  branch only, so a line naming a `linecode` and also stating inline
  `R_series_1_1` matrices matched exactly one branch and was accepted, against
  the specification's "exactly one impedance source". Both branches now exclude
  the other shape, so the two are disjoint.

## 0.1.0

The draft schema published in
[`distribution-system-opt/bmopf-resources`](https://github.com/distribution-system-opt/bmopf-resources)
as `draft_schema_and_networks/draft_bmopf_schema.json`. Not released from this
repository; recorded here as the base 0.2.0 extends.

### Explicit exciting-branch location and conformance evidence

- Add the optional `no_load_shunt` object with a physical winding index and
  per-coil siemens, mutually exclusive with the existing from-side fields.
  Existing data retains its meaning. This represents the OpenDSS winding-2
  exciting branch without an approximation across transformer leakage.
- Add a worked example, schema and semantic checks, expanded field-by-field
  implementation/evidence columns, and six independent OpenDSS stamp comparisons.
- Keep proposal status explicit; publication of PowerIO does not ratify BMOPF.
