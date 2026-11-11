# BMOPF data schema

BMOPF gives distribution-system datasets a shared, explicit description of
conductors, equipment and operating limits. This repository accompanies the
[Task Force's mathematical and data-model specification](https://github.com/distribution-system-opt/math-and-data-model-specifications).

**This branch proposes a versioned BMOPF v0.2.0, subject to Task Force approval.**
It brings together the community's schema and specification work since v0.1.0,
including [Matt Deakin's source and objective proposal](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/36).
Findings from developing a reference implementation in PowerIO v0.11.0 provide
additional examples, compatibility checks and questions for review.

The [contribution record](contributors.md) credits the work this proposal
builds on. [Alignment with existing proposals](upstream-alignment.md)
identifies adopted definitions, additional findings and open questions.

## Proposed scope

Alongside the current source and objective changes, this draft proposes clearer
units, conductor ordering and validation, plus additional transformer winding,
tap, neutral and core-shunt data. It also reconsiders inverter controls, line
construction data, DC equipment, time-series fields and element geometry
(GeoJSON points and routes for every element with a place on the map, with one `meta.crs`) explored in earlier
Task Force drafts and in BMOPFTools PR 258. Their earlier removal limited the scope of v0.1.0; their
inclusion here is a proposal for review, not an accepted expansion of scope.
[Changes and compatibility](../CHANGELOG.md) describe the additions individually.

The schema defines structure. The accompanying proposed specification supplement
describes the intended semantics. Neither a field's presence nor successful
parsing proves that a particular solver implements it. PowerIO's release does
not determine the Task Force's decisions or release schedule.

## Start with a small feeder

[worked_feeder.json](../examples/0.2.0/worked_feeder.json) describes two four-terminal
buses, a 100 m cable, a fixed voltage source and three unequal phase loads.

- `terminal_names` fixes bus order as `a, b, c, n`.
- The line maps corresponding terminals in that same order at both ends.
- Cable resistance is 0.001 ohm/m per conductor, hence 0.1 ohm over the line.
- The source fixes phase-to-ground magnitudes to 230 V and neutral to 0 V.
- Load powers are 1000, 800 and 1200 W, in phase order.
- Source energy prices are 0.10 $/kWh for each phase, with no neutral entry.
- The load bus's minimum magnitudes are 210, 212 and 214 V. The neutral has
  its separate 10 V cap; it does not receive a fourth phase bound.

[Field semantics](semantics.md) explains the less obvious conventions.
[The field inventory](fields.csv) lists every proposed field, and
[the conformance packet](conformance.md) distinguishes preserved data,
validated data and supported calculations.

## Validate structure and semantics

```sh
python3 -m pip install jsonschema
python3 tests/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

Structural validation checks types, required fields and permitted names.
`tests/semantics.py` additionally checks dimensions, terminal roles, references,
matrix indices and bounds. Historical examples keep their original content;
known semantic findings are pinned in the tests rather than silently repaired.
A computational consumer must perform its own capability and numerical checks
before solving a case.

Unknown electrical fields are rejected. Two extension locations are deliberately
free-form: top-level `extras` and `meta.provenance`. Existing provenance keys
remain legitimate. A conversion that relocates required physics into `extras`
must report that relocation; consumers cannot assume that ignoring it preserves
the original calculation.

## Identify a document

A document states `meta.schema_version`, the release it was written against, and
nothing else identifies its version. The schema accepts any 0.2.x value, so a
0.2.0 document remains valid when 0.2.1 adds optional content, and a 0.2.1
document that uses nothing new validates under 0.2.0. The schema's own `$id` is
the URL of its bytes at the `schema-v0.2.0` tag; it names the schema, not the
document. Retrieval and audit data (a draft commit, the schema digest) belong in
`meta.provenance`.

Why: PowerIO 0.11 stamped an archive URL of its own in `meta.$schema`, and
BMOPFTools allow-listed accepted URLs one by one, so valid documents failed intake
over a string ([BMOPFTools #487](https://github.com/frederikgeth/BMOPFTools.jl/issues/487)).
Fixing `meta.$schema` to one URL per release would have moved the same problem to
patch releases: a 0.2.1 schema could not accept a 0.2.0 document. A version
string checked by a line pattern is what OpenAPI (`openapi`), glTF
(`asset.version`), CycloneDX (`specVersion`) and CityJSON (`version`) use.

| Identifier | Meaning |
|---|---|
| `meta.version` | Dataset revision chosen by its author |
| `meta.schema_version` | BMOPF release the document was written against |
| Draft commit and schema digest, in `meta.provenance` | Exact bytes a producer used before the tag |
| Producer version (for example PowerIO 0.12) | Implementation that wrote the document |

Only the Task Force releases a `schema-v0.2.0` tag. Proposed directories may
change during review; a released schema directory is immutable.

## Repository layout and contribution

```text
schema/bmopf/0.2.0/   proposed JSON Schema
examples/0.2.0/       historical and authored examples
contracts/           compatibility expectations
tests/              structural and semantic checks
docs/               semantics, contributor credits and validation evidence
```

Follow [CONTRIBUTING.md](../CONTRIBUTING.md) and the specification repository's
paired-change workflow for changes to fields or their meaning. Substantial
mathematical explanations belong in that specification, with links here.

Schema and documentation contributions use [CC BY 4.0](../LICENSE). Network
examples retain their own licences in `meta.license` or the accompanying source
record. Cite the exact proposal commit for reproducibility, and a release tag
once one exists.
