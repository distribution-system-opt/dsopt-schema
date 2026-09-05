# PowerIO integration conformance packet

This packet accompanies the proposed BMOPF 0.2.0 schema and the integration
being prepared for PowerIO v0.11.0. Ratification remains a Task Force decision.

## Frozen comparison inputs

[contracts/field-baselines.json](../contracts/field-baselines.json) records source
URLs, byte digests and field paths for these inputs:

| Input | Revision |
|---|---|
| Archived complete BMOPF draft | `bmopf-resources` `2e0b1cba27a279cbf430836f1cd0cb4370887109` |
| PowerIO's legacy 0.1.0 schema | PowerIO `ca8cfcec8bdc35d083dfc91b0bb9025ac8bb7507` |
| Proposal before this integration | `dsopt-schema` `f9e0802bf1d510abaa97a5731ce14c3eb3373e6d` |
| Accepted mathematical/data specification | `73fae2b6bae2663d9a2e901c41a4c062457bf834` |
| Public BMOPFTools comparison baseline | `4c4dafdd2b1a36541f2d1a068b01bdcc6dfcfc3a` |

The proposal baseline and PowerIO v0.11.0's originally vendored proposal have
identical decoded JSON content. This update therefore checks semantic and
behavioral differences rather than claiming that merely copying the schema
establishes conformance.

`python3 tests/field_inventory.py --check` verifies [fields.csv](fields.csv),
which expands references into field/table paths with exact types,
requiredness, schema defaults and descriptions (including units/order).
Presence flags compare each field against all three structural baselines.
An absent schema default is not an invented electrical default.

## Preservation, validation and calculation

| Data | PowerIO reader / IR | Explicit writer | Computational contract and evidence |
|---|---|---|---|
| Schema identifiers | Resolve known version aliases; report contradictions | Selected profile overrides retained-source echo | Version consistency regression; producer provenance pins proposal bytes |
| Metadata / provenance | Preserve source metadata independently of electrical tables | Keep legitimate `meta.provenance` and `extras` | Metadata is excluded from semantic equipment traversal |
| Bus terminals / phase bounds | Preserve order and unequal per-phase values in generation-2 IR | Emit full phase arrays; PMD uses terminal order and kV conversion | Phase-dimension, unresolved-ground and IR-without-source regressions |
| Lines / linecodes | Typed conductor matrices and ordered end maps | Per-metre versus absolute impedance remains explicit | Shape/reference tests; passive matrix analytical tests |
| Loads / sources / generators | Typed powers, voltage specifications and cost fields | Per-phase or per-terminal ordering follows each field | Dimensions and model capability must be checked before solving |
| Two-winding transformers | Typed winding connections, ratios and neutral impedances; retained core metadata | Proposal tap spellings and side-specific units | Fixed ideal grounded-WYE matrix profile is limited; unsupported required equations must fail explicitly |
| Regulators / n-winding data | Typed or retained according to each supported subtype | Top-level proposal subtypes; legacy relocation reports | Retention alone does not establish a tap-control or n-winding solver |
| Inverter controls | Typed IBRs and control profiles | Proposal tables; legacy `extras` relocation | A consumer must advertise its supported controls and DC coupling |
| Wire data / geometry | Construction/provenance retention and supported conversion | Preserve or diagnose unsupported projection | A supplied linecode is distinct from calculating it from geometry |
| DC / time profiles | Retain tables and field references | Proposal tables; legacy relocation reports | Requires a DC-capable formulation or an explicitly selected time state |

The table identifies the integration paths, not a blanket certification of every
numerical field. The final release review packet must include the exact PowerIO
and consumer revisions and the independent numerical comparisons. No solver
support should be inferred from a parsing or schema-validation result.

## Tested compatibility statement

The structural suite validates the historical ENWL file, the component example
and the authored worked feeder and transformer. Twenty negative files exercise structural
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
and explicit-profile tests, C ABI tests, and multiconductor matrix tests. Tests
must emit from changed or deserialized values as well as retained sources: a
byte-exact echo does not test a writer's electrical conversion.

BMOPFTools is publicly available and participates in the comparison. Its
baseline depends on PowerIO.jl 0.9; the coordinated compatibility follow-up
moves its ingestion to typed 0.11 modules. Numerical comparisons must include
independently authored BMOPF inputs and analytical expectations so shared
PowerIO ingestion cannot conceal a common conversion error.
