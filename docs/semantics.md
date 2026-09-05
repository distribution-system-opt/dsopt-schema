# Proposed field semantics

This document summarizes the proposed 0.2.0 contract. The
[specification supplement](https://github.com/distribution-system-opt/math-and-data-model-specifications/blob/propose-bmopf-0.2.0/docs/src/proposals/bmopf-0.2.0.md)
contains the proposed mathematical relations. Both remain subject to Task Force
review. The machine-readable [field inventory](fields.csv) is generated from
this branch's schema, so exact names and descriptions can be checked together.

## Units and identity

Electrical input uses absolute SI quantities: V, A, W, var, VA, ohm, S, m and
rad. Frequencies use Hz. No global base or per-unit scaling is implicit.
A linecode's impedance/admittance is per metre; inline line matrices are
absolute for the complete line. A line must choose exactly one source.

Table keys identify equipment. A terminal map names bus terminals and fixes
conductor order. The `from` and `to` maps of a line or switch have equal length;
position k connects to position k, even when the terminal labels differ.
Matrix indices are one-based in this order. A stated triangle can supply its
mirror; absent off-diagonal entries are zero. Consumers must not silently
truncate oversized matrices or pad mismatched conductor maps.

When `terminal_conventions` exists, its disjoint role lists are authoritative
and case-sensitive. Otherwise `n` and `N` are neutrals, and `4` is neutral on a
bus whose terminal set is exactly `1,2,3,4`. Other names are phases. The ground
reference `g` is implicit and does not become an extra bus terminal. Earth
wires are explicit conductors, with their impedance and connections retained.

## Voltage, current and power arrays

Bus `v_min`/`v_max` and `vpn_min`/`vpn_max` contain one value per phase, in bus
terminal order with nonphase terminals omitted. Unequal entries remain unequal.
`vn_max` separately limits neutral-to-ground magnitude. `vpp_min`/`vpp_max`
use phase pairs, including the three-phase order `(1,2), (2,3), (3,1)`.
Sequence constraints require their stated three-phase interpretation.
An absent bound imposes no corresponding limit.

A voltage source's magnitude and angle arrays include every entry in its
terminal map, including an explicitly fixed neutral. Load powers describe
sub-loads: phase-to-neutral branches for WYE, one terminal pair for
SINGLE_PHASE, and phase-pair branches for DELTA. Generator power limits and
linear cost coefficients follow phase order. Current limits follow the
conductor or winding-side order declared on the field, not a common voltage
base. The schema describes the optional neutral-return generator current entry.

## Transformers and regulators

| Field family | Proposed interpretation |
|---|---|
| Two-winding `tap_ratio` | Dimensionless multiplier on the nameplate ratio |
| `tap_ratio_min`/`tap_ratio_max` | Permitted ratio interval; unequal limits request a tap decision |
| `r_series_from`/`x_series_from`, `r_series_to`/`x_series_to` | Ohms on the named winding side |
| Wye/delta `r_series`/`x_series` | Ohms referred to the wye-side winding |
| `r_neutral_*`/`x_neutral_*` | Winding-neutral-to-earth impedance in ohms |
| `g_no_load`/`b_no_load` | From-side core shunt in siemens; inductive susceptance is negative |
| `i_max_from`/`i_max_to` | Limits on the corresponding side's currents in amperes |
| `n_winding.windings` | Ordered windings; winding 1 establishes the reference |
| Regulator `tap_ratio` | Regulation ratio, with type A/B relation defined by its subtype |

Three-phase nameplate voltages are line-to-line quantities. Coil voltages must
account for the winding connection; a WYE coil uses the line-to-neutral voltage.
A single-phase or split winding follows its own stated nominal-voltage field.
Do not apply a square-root-of-three conversion to every transformer uniformly.

The proposal spells two-winding tap fields `tap_ratio`, `tap_ratio_min` and
`tap_ratio_max`. PowerIO reads its earlier `tap` spellings as documented
compatibility aliases and emits the proposal spellings on explicit conversion.
A retained, unmodified source may still reproduce its original spelling.

A regulator or variable tap is more than a fixed turns ratio. A fixed-tap
admittance calculation must reject a requested tap optimization that it cannot
perform. Likewise, retaining n-winding parameters does not establish that a
specific solver implements the full equivalent circuit.

The [worked transformer](../examples/0.2.0/worked_transformer.json) has a
10 kVA common short-circuit base and winding ratings of 9, 8 and 2 kVA. Its
primary resistance is 2 ohm, with a 1.02 tap and a 5+j1 ohm neutral branch.
The winding ratings do not change the declared common `x_sc` base. An absent
neutral-impedance pair adds no internal grounding branch; an explicitly zero
pair gives solid grounding.

## Extensions, legacy output and validation

`meta.provenance` carries arbitrary producer/audit metadata. Top-level `extras`
can retain data outside the selected schema version. Neither is a place to
hide an unreported electrical loss.

PowerIO's explicit 0.1.0 output relocates proposed-only tables and regulator or
n-winding subtypes into `extras`, and reports each relocation. Extra transformer
parameters are keyed by subtype and equipment ID. Its reader merges those
recognized overlays back into typed data, with the standard field taking
precedence on a collision. A generic 0.1.0 consumer that ignores these overlays
cannot be assumed to solve an equivalent system.

Validation has four separate results:

1. Parsing: bytes were decoded and retained or converted.
2. Structural validity: fields and types satisfy the selected JSON Schema.
3. Semantic validity: references, dimensions, ordering and bounds are consistent.
4. Computational capability: the selected formulation implements all required
   physics, controls and constraints.

No earlier result implies a later one. Numerical validation additionally checks
solutions and invariants using independent inputs and implementations.

## Cross-field validation details

Terminal identities are case-sensitive. Explicit role lists take precedence;
without them, `n` and `N` are neutral labels, and terminal `4` in the complete
`1,2,3,4` convention is neutral. Phase limit vectors retain bus order after
excluding neutral and earth terminals. Unused terminals remain meaningful
connection points and are preserved by the PowerIO writer. An element map may
repeat a bus terminal: parallel physical conductors can connect to the same
phase node. Their conductor positions and matrix rows remain distinct.

DC end maps must refer to terminals on the named DC buses. Per-conductor
resistance, current limits, and the opposite end map have matching lengths.
The `pole` keys and grounded-terminal list must belong to their DC bus.

A `line_geometry` conductor names an existing `wire_data` entry. A linecode's
optional `line_geometry` back-reference must resolve. An n-winding `x_sc` table
contains every pair `i_j`, with `1 <= i < j <= winding_count`; no missing pair
is interpreted as a measured zero.

Each time-profile mapping names an existing profile and a stated numeric field
on the element. A profile's optional time axis has the same length as its
values and increases strictly. Consumers must select a step and check that
referenced profiles share the same step grid before evaluating a time state.

## Explicit transformer core shunts

`no_load_shunt` names a physical winding and states its per-coil admittance in
siemens. It is mutually exclusive with `g_no_load` and `b_no_load`. Omitting the
object preserves the existing from-side convention of those fields (winding 1
for `n_winding`); no input receives a new default shunt.

```json
"no_load_shunt": {"winding": 2, "g": 0.001, "b": -0.002}
```

For a 100 V coil this object consumes 10 W and 20 var. Each coil on winding 2
receives the stated admittance. The object specifies the terminal-coil branch
at the operating tap: changing a tap does not implicitly rescale its physical
siemens. Two-winding objects count from and to as 1 and 2. A centre-tapped
secondary counts its first leg as 2 and its second leg as 3. An n-winding
object uses its declared winding order.

The distinction matters because OpenDSS places its exciting branch on winding
2. Moving it to winding 1 through a turns-ratio calculation is not exact when
leakage is nonzero. The explicit object preserves that branch at its physical
location. WYE three-phase coil voltage is line-to-line voltage divided by the
square root of three; a DELTA coil uses line-to-line voltage. A positive
OpenDSS magnetizing-current percentage yields negative susceptance.

[The worked transformer](../examples/0.2.0/worked_transformer_shunt.json) and
[the conformance packet](conformance.md#independent-core-shunt-comparison)
provide data and numerical checks. Consumers that cannot model this branch
must reject the requested calculation or make a documented exact conversion,
such as a bus-shunt stamp with the same coil incidence.

## Energy prices and objective units

`energy_cost_rate` states the price of injected active energy in $/kWh.
Generator and IBR vectors follow phase order. A voltage source's vector follows
its complete `terminal_map`, including any neutral terminal. Source injections
use the same positive-generation convention as generator injections. A source
can supply or absorb current independently at each fixed terminal; its neutral
must not acquire a generator-only zero-current constraint.

For one hour at 1000 W injection, a rate of 0.10 $/kWh contributes $0.10.
For an interval of `duration_hours`, the contribution is
`duration_hours * sum(energy_cost_rate * p_injected_w) / 1000`.
The interval belongs to the calculation, not the network's dataset version.
These choices follow the coordinated
[source and objective discussion](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/36)
and [data-field proposal](https://github.com/distribution-system-opt/bmopf-resources/pull/21).

The deprecated `cost` spelling remains accepted with its stated per-phase
ordering. For a voltage source it expands to terminal order with zero at
nonphase terminals. Supplying both names requires equal rates after that
expansion. Fresh draft BMOPF 0.2 output uses `energy_cost_rate`. Explicit 0.1.0
output uses generator `cost` and preserves source prices in the documented
`extras.voltage_source` overlay, because that schema has no source-price field.
A generic 0.1.0 consumer must not assume that it has loaded those prices.
