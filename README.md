# BMOPF data schema

BMOPF gives distribution-system datasets a shared, explicit description of
conductors, equipment and operating limits. This repository accompanies the
[Task Force's mathematical and data-model specification](https://github.com/distribution-system-opt/math-and-data-model-specifications).

**This branch proposes BMOPF 0.2.0. It is not a ratified release.** PowerIO
v0.11.0 is preparing support for a pinned revision of this proposal. Shipping
an implementation does not determine the Task Force's modelling decisions.
Feedback on those decisions and on interoperability is welcome.

## What the proposal adds

The proposal describes regulator taps, winding neutral impedances, transformer
magnetizing terms with an explicit coil location and n-winding equipment, together with inverter controls,
line construction provenance, DC data and named time profiles. It also makes
units and conductor ordering explicit and fills missing cost fields referenced
by the OPF objective. [Changes and compatibility](CHANGELOG.md) explain the
individual additions.

The schema defines structure. The accompanying proposed specification supplement
describes the intended semantics. Neither a field's presence nor successful
parsing proves that a particular solver implements it.

## Start with a small feeder

[worked_feeder.json](examples/0.2.0/worked_feeder.json) describes two four-terminal
buses, a 100 m cable, a fixed voltage source and three unequal phase loads.

- `terminal_names` fixes bus order as `a, b, c, n`.
- The line maps corresponding terminals in that same order at both ends.
- Cable resistance is 0.001 ohm/m per conductor, hence 0.1 ohm over the line.
- The source fixes phase-to-ground magnitudes to 230 V and neutral to 0 V.
- Load powers are 1000, 800 and 1200 W, in phase order.
- The load bus's minimum magnitudes are 210, 212 and 214 V. The neutral has
  its separate 10 V cap; it does not receive a fourth phase bound.

[Field semantics](docs/semantics.md) explains the less obvious conventions.
[The field inventory](docs/fields.csv) lists every proposed field, and
[the conformance packet](docs/conformance.md) distinguishes preserved data,
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

## Pin a proposal reproducibly

The schema's `$id` is its canonical identity. Retrieval is separate: a producer
supporting this proposal should write an immutable raw GitHub commit URL in
`meta.$schema`, then record the proposal commit, SHA-256 of the schema bytes and
`status: "proposal"` in `meta.provenance`. Retrieve and verify that exact file
rather than following a moving branch. Older canonical identifiers remain
readable aliases, not evidence that 0.2.0 was ratified.

These versions answer different questions:

| Identifier | Meaning |
|---|---|
| `meta.version` | Dataset revision chosen by its author |
| `meta.schema_version` | BMOPF structural/semantic profile |
| Proposal commit and schema digest | Exact reviewed proposal snapshot |
| PowerIO v0.11.0 | Producer implementation version |
| PowerIO IR generation 2 | PowerIO's own serialized module layout |
| PowerIO C ABI 7 | Native binding contract |

Only the Task Force releases a `schema-v0.2.0` tag. Proposed directories may
change during review; a released schema directory is immutable.

## Repository layout and contribution

```text
schema/bmopf/0.2.0/   proposed JSON Schema
examples/0.2.0/       historical and authored examples
contracts/           compatibility expectations
tests/              structural and semantic checks
docs/               semantics, field inventory and integration evidence
```

Follow [CONTRIBUTING.md](CONTRIBUTING.md) and the specification repository's
paired-change workflow for changes to fields or their meaning. Substantial
mathematical explanations belong in that specification, with links here.

Schema and documentation contributions use [CC BY 4.0](LICENSE). Network
examples retain their own licences in `meta.license` or the accompanying source
record. Cite the exact proposal commit for reproducibility, and a release tag
once one exists.
