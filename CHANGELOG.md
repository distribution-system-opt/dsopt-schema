# Changelog

Notable changes to the BMOPF JSON Schema.

## 0.2.0 (proposed, subject to Task Force approval)

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
round-trip checks record the evidence and its limits. PowerIO, BMOPFTools and
OpenDSS provide implementation comparisons; publication of any implementation
does not ratify BMOPF.

## 0.1.0

The schema identified as 0.1.0 in
[`bmopf-resources`](https://github.com/distribution-system-opt/bmopf-resources)
at `draft_schema_and_networks/draft_bmopf_schema.json` provides the historical
baseline. It was not released from this repository. The
[contribution record](docs/contributors.md) identifies the dated source history
without treating the specification PDF's version as the JSON Schema version.
