# BMOPF v0.2.0 compatibility and implementation evidence

This packet supports Task Force review of a versioned BMOPF v0.2.0. It records
findings from developing a reference implementation in PowerIO v0.11.0 and
direct comparisons with OpenDSS. Ratification remains a Task Force decision.

## Frozen comparison inputs

[contracts/field-baselines.json](../contracts/field-baselines.json) records source
URLs, byte digests and field paths for these inputs:

| Input | Revision |
|---|---|
| Archived complete BMOPF draft | `bmopf-resources` `2e0b1cba27a279cbf430836f1cd0cb4370887109` |
| Historical Task Force 0.1.0 schema | `bmopf-resources` `f2e368470a5012dd264d1f5a2f867867fb926615` |
| Initial versioned proposal | `dsopt-schema` `3632a88c972427c888db622ffc3f706dd61719b6` |
| Specification main snapshot (unreleased) | `73fae2b6bae2663d9a2e901c41a4c062457bf834` |

The proposal baseline and PowerIO v0.11.0's originally vendored proposal have
identical decoded JSON content. This update therefore checks semantic and
behavioral differences rather than claiming that merely copying the schema
establishes conformance.

`python3 tests/field_inventory.py --check` verifies [fields.csv](fields.csv),
which expands references into field/table paths with exact types,
requiredness, schema defaults and descriptions (including units/order).
Presence flags compare each field against all three structural baselines. Each row also identifies its specification chapter, reading/preservation path, explicit writer behavior, calculation limitations, validation and test evidence. Numerical evidence is identified separately from structural family coverage.
An absent schema default is not an invented electrical default.

## Preservation, validation and calculation

| Data | PowerIO reader / IR | Explicit writer | Computational support and evidence |
|---|---|---|---|
| Schema identifiers | Resolve known version aliases; report contradictions | Selected schema version overrides retained-source echo | Version consistency regression; producer provenance pins proposal bytes |
| Metadata / provenance | Preserve source metadata independently of electrical tables | Keep legitimate `meta.provenance` and `extras` | Metadata is excluded from semantic equipment traversal |
| Bus terminals / phase bounds | Preserve order and unequal per-phase values in generation-2 IR | Emit full phase arrays; PMD uses terminal order and kV conversion | Phase-dimension, unresolved-ground and IR-without-source regressions |
| Lines / linecodes | Typed conductor matrices and ordered end maps | Per-metre versus absolute impedance remains explicit | Shape/reference tests; passive matrix analytical tests |
| Loads / sources / generators | Typed powers, voltage specifications and cost fields | Per-phase or per-terminal ordering follows each field | Dimensions and model capability must be checked before solving |
| Two-winding transformers | Typed winding connections, ratios and neutral impedances; retained core metadata | Proposal tap spellings and side-specific units | Fixed ideal grounded-WYE matrix profile is limited; unsupported required equations must fail explicitly |
| Regulators / n-winding data | Typed or retained according to each supported subtype | Top-level proposal subtypes; legacy relocation reports | Retention alone does not establish a tap-control or n-winding solver |
| Inverter controls | Typed IBRs and control profiles | Proposal tables; legacy `extras` relocation | A consumer must advertise its supported controls and DC coupling |
| Wire data / geometry | Construction/provenance retention and supported conversion | Preserve or diagnose unsupported projection | A supplied linecode is distinct from calculating it from geometry |
| DC / time profiles | Retain tables and field references | Proposal tables; legacy relocation reports | Requires a DC-capable formulation or an explicitly selected time state |

The table identifies the implementation paths, not a blanket certification of every
numerical field. The final release review packet must include the exact PowerIO
and consumer revisions and the independent numerical comparisons. No solver
support should be inferred from a parsing or schema-validation result.

## Tested compatibility statement

The structural suite validates the historical ENWL file, the component example
and the authored worked feeder and transformer. Twenty-one negative files exercise structural
rejections. The semantic suite additionally exercises conflicting versions,
role-list overlap, phase-array length, unequal end-map length, unknown references,
oversized matrix indices, inconsistent tap bounds, DC terminal references,
geometry-library references, complete short-circuit pair tables, and
time-profile references and ordering.

The historical ENWL source bus lists terminal `5` as perfectly grounded while
its `terminal_names` are `a,b,c,n`. Its exact bytes and this finding are pinned in
[contracts/historical.json](../contracts/historical.json). The historical file
is kept intact. It passes JSON Schema structure but is not a semantically valid
numerical input until its author chooses the intended grounding repair.

Intentional rejection changes are explicit: an ambiguous line with both a
linecode and inline impedance; contradictory version declarations; array lengths
that disagree with conductor order; invalid electrical references; inconsistent
bounds; and requested physics outside a consumer's declared formulation.
Legitimate free-form provenance is not rejected.

## Reproduce the schema checks

```sh
python3 -m pip install jsonschema
python3 tests/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 tests/field_inventory.py --check
```

PowerIO regression commands include the BMOPF/PMD conversion suites, facade IR
and explicit schema-version tests, C ABI tests, and multiconductor matrix tests. Tests
must emit from changed or deserialized values as well as retained sources: a
byte-exact echo does not test a writer's electrical conversion.

Numerical evidence must include independently authored inputs and analytical
expectations so shared ingestion cannot conceal a common conversion error.
Implementation comparisons inform review; they do not define Task Force scope.

## Independent core-shunt comparison

PowerIO's `evals/validation/validate_bmopf_core_shunts.py` generates six small
OpenDSS cases, serializes each to generation-2 IR, and emits the BMOPF proposal
from that IR. Retained source bytes cannot bypass the writer. The comparison
subtracts OpenDSS's no-load-off transformer `Yprim` from its no-load-on `Yprim`,
then compares that difference with an independently assembled BMOPF coil stamp.

The cases cover WYE/DELTA, DELTA/WYE, decomposed WYE/WYE, a phase-to-phase pair,
a centre tap and four windings, including off-nominal taps. The observed maximum
absolute discrepancy is below `7e-15 S`; the declared tolerance is
`1e-10 S + 1e-9 * max(abs(Y_shunt))`. This establishes the exciting-branch
location, sign, phase scaling and tap scaling. It does not certify every
transformer's leakage network, regulator controller or OPF formulation.

The implementation follows the separate exciting-branch stamp in
[DSS C-API Transformer.pas](https://github.com/dss-extensions/dss_capi/blob/87d85c2622c8281b92255335bc7c09b11191b21d/src/PDElements/Transformer.pas).

## Complete four-winding reactances

PowerIO's `a84d97d97343b4175e9a846aa358997ff53b0e5f` candidate preserves all
OpenDSS `Xscarray` pairs through its typed model, IR, BMOPF and regenerated DSS.
The reader respects OpenDSS edit boundaries and the writer emits every pair.
These preservation checks do not certify a general n-winding OPF formulation.

## Energy-price compatibility

Draft BMOPF 0.2 accepts `energy_cost_rate` and the deprecated `cost` spelling.
The required generator price remains required: either spelling satisfies it.
Rates remain $/kWh; no existing coefficient receives a numerical rescaling.
Source prices follow phase order, matching Matt Deakin's source page;
neutral terminals have no price entry. Conflicting spellings and incorrect vector lengths are
semantic errors. Fresh draft output uses the proposed name.

PowerIO's `energy_costs_keep_phase_order_through_mutation_ir_and_schema_conversion`
test changes a source price, serializes the network to IR, and checks both 0.1.0
and draft output. C tests read the borrowed price span after the module handle
is freed; Julia checks the vector after IR restoration and garbage collection.
IBR prices remain retained fields, and their presence does not claim that a
consumer implements inverter controls or optimizes an IBR objective.

Unresolved OpenDSS geometry deliberately blocks numerical calculation and
canonical export. Retaining source objects is not equivalent to calculating
conductor impedances. This distinction is covered by the PowerIO readiness and
facade integration tests associated with contributor PR #494.

The versioned import and its exact provenance are documented in the
[baseline record](baseline-0.1.0.md). The metadata wording discrepancy is tracked
separately in [specification #41](https://github.com/distribution-system-opt/math-and-data-model-specifications/issues/41);
this comparison does not change the historical schema to resolve it.
