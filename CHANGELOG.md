# Changelog

Notable changes to the BMOPF JSON Schema.

## 0.2.0 (proposed, subject to Task Force approval)

### Task Force review answers (2026-11-11)

- `vpg_min`/`vpg_max` have one entry per phase terminal (confirmed).
- Bus `vn_max` is renamed `vng_max`, the neutral-to-ground bound, matching the
  `vpg` (phase-to-ground) naming. `vn_max` is rejected in 0.2.0 documents.
- `meta.$schema` is fixed to the version's `$id` (confirmed).
- Every element with a place on the map can carry `geo`. Sources, loads,
  generators, inverters, shunts, capacitors, DC buses, DC loads, DC sources and
  DC grounding take a GeoJSON Point. Switches, every transformer type and DC
  branches take a Point (their site) or a LineString (their route between buses).
  Every `geo` may carry a GeoJSON `bbox`. All of it is optional and descriptive.

### Reconciliation with 0.1.1, geometry and one identifier (2026-11-10)

- Bus phase-to-ground bounds take the 0.1.1 names `vpg_min`/`vpg_max`
  ([schema #6](https://github.com/distribution-system-opt/dsopt-schema/pull/6),
  [specification issue #51](https://github.com/distribution-system-opt/math-and-data-model-specifications/issues/51)):
  `v_min`/`v_max` was ambiguous between phase-to-ground and phase-to-neutral. The
  proposal keeps its array semantics (one entry per phase terminal, the neutral
  bounding through `vng_max`), which differs from the 0.1.0/0.1.1 wording "one
  entry per bus terminal"; the Task Force confirmed per phase terminal on 2026-11-11.
  `v_min`/`v_max` are rejected in 0.2.0 documents.
- Geometry gets typed slots: `bus.*.geo` (GeoJSON Point), `line.*.geo` (GeoJSON
  LineString) and `meta.crs` (authority code; absent means WGS84). The fields
  follow [BMOPFTools PR #258](https://github.com/frederikgeth/BMOPFTools.jl/pull/258)
  and the shape PowerIO already reads; PowerIO 0.11 had to write the same data as
  a FeatureCollection under `extras.geojson` because no slot existed, and every
  consumer then needed a sideload path. Geometry is descriptive: no calculation
  reads it.
- `meta.$schema` is the schema's canonical `$id` (`const`). Producers used to
  stamp per-producer archive URLs so the exact bytes could be retrieved, and each
  consumer allow-listed URLs one by one
  ([BMOPFTools #487](https://github.com/frederikgeth/BMOPFTools.jl/issues/487)).
  Retrieval permalinks and digests belong in `meta.provenance`.
- Merged `main` (schema 0.1.1 and its fixtures) into the proposal, so one
  lineage continues from 0.1.1 to 0.2.0.

This versioned proposal builds on the Task Force's schema and specification
work since v0.1.0. [Contributor credits](docs/contributors.md) identify that work;
[proposal alignment](docs/upstream-alignment.md) separates existing definitions
from additional findings developed through a reference implementation in
PowerIO v0.11.0. No proposed modelling choice is accepted until Task Force review.

### Current source and objective proposals

- Adopt per-phase `energy_cost_rate` in $/kWh for sources and generators from
  Matt Deakin's coordinated [specification #36](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/36)
  and [schema #21](https://github.com/distribution-system-opt/bmopf-resources/pull/21).
  Neutral terminals have no price entry; source voltage vectors still include
  every terminal.
- Retain `cost` as a deprecated spelling with the same values and ordering.
  Either spelling satisfies the required generator-price field. If both occur,
  they must agree. No coefficient receives a numerical rescaling.
- Keep source-current signs, KCL and the one-hour objective in the source and
  objective proposal. Optional IBR price data is an additional proposed field;
  it does not change that proposal's source/generator objective.

### Additional equipment data proposed for review

The archived schema in `bmopf-resources` at `2e0b1cb` explored equipment later
set aside in `afda547` and `9c9b26f` to limit the scope of v0.1.0. This proposal
reconsiders that material using the current units and conventions. Inclusion
here does not reverse the Task Force's earlier scope decisions.

- Inverter-based resources and reusable Volt-VAr, Volt-Watt and power-factor
  controls, with explicit phase/conductor ordering and optional DC coupling.
- Wire and cable construction data, line geometry and linecode derivation
  provenance, including the declared frequency and earth-model assumptions.
- DC buses, branches, grounding, loads and sources.
- Named time-series data and references from equipment fields.
- N-winding transformers, ordered winding ratings, taps and neutral impedances,
  and complete pairwise short-circuit reactances on a declared common base.
- Single-phase autotransformer and open-delta regulator subtypes, with stated
  tap conventions and bounds. Open-delta tap arrays contain two entries.
- Two-winding tap multipliers, winding-side neutral impedances and from-side
  magnetizing admittances. An absent internal neutral branch remains distinct
  from explicitly solid grounding.
- An optional `no_load_shunt` object with a physical winding index and per-coil
  siemens, mutually exclusive with the existing from-side shunt fields. Six
  independent OpenDSS comparisons test its location, sign and scaling.
- Optional source active-power bounds and IBR energy-price data.

### Proposed clarifications and validation

- State array lengths and order for each field: bus bounds follow phase order,
  load powers follow sub-load order, source voltages follow terminal order,
  and matrices follow component connection order.
- State transformer ratios, winding-side units and current-limit conventions.
  The paired specification supplement describes the proposed interpretations.
- Document ideal equipment equations in the specification supplement rather
  than treating an arbitrary small impedance as an exact ideal constraint.
- Add semantic checks for contradictory schema identifiers, role-list overlap,
  dimensions, references, matrix indices, tap bounds and time-series data.
- Reject lines that simultaneously supply inline impedance and a linecode.
- Separate canonical schema identity from immutable draft retrieval. Keep
  dataset version, schema version and producer version independent.
- Preserve both metadata extension locations: top-level `extras` and
  `meta.provenance`. Unknown electrical fields remain rejected.
- Propose an explicit earth-terminal role while leaving the wider terminal-role
  taxonomy open in the existing Task Force discussion.

### Compatibility and evidence

Compatibility is checked against named inputs in the
[conformance packet](docs/conformance.md), not asserted as a blanket superset.
The historical ENWL example passes structural validation; semantic validation
reports its existing reference to an undeclared grounded terminal. Its bytes
remain unchanged.

Intentional rejection changes include ambiguous impedance sources,
contradictory version declarations, invalid array dimensions, unresolved
references and inconsistent bounds. A consumer separately checks whether it
supports required physics. Parsing or preserving a field does not establish
that a solver models it.

The worked feeder, transformer examples, field inventory and mutation/IR
round-trip checks record the evidence and its limits. PowerIO and
OpenDSS provide implementation comparisons; publication of any implementation
does not ratify BMOPF.

## 0.1.1

Rename bus `v_min`/`v_max` to `vpg_min`/`vpg_max` following Robert Ferrando's
review in
[specification issue #51](https://github.com/distribution-system-opt/math-and-data-model-specifications/issues/51)
(Matt Deakin, [schema #6](https://github.com/distribution-system-opt/dsopt-schema/pull/6)).
No other field changes; fixtures and rejected inputs mirror 0.1.0.

## 0.1.0 (historical baseline, not a release)

Import the Task Force schema at `bmopf-resources` commit
`f2e368470a5012dd264d1f5a2f867867fb926615`. Only `$id` changes to identify its
versioned location. Field names, types, required fields, and validation rules
remain unchanged. Add source provenance, small structural examples, and checks.

The specification PDF's version is independent of this JSON Schema version.
See [source history and credits](docs/baseline-0.1.0.md).
