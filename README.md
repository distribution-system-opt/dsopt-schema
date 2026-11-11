# BMOPF JSON schemas

This repository hosts JSON schemas for the IEEE PES Task Force on Benchmarking
Multiconductor OPF for Distribution Systems. The accompanying
[mathematical and data-model specification](https://github.com/distribution-system-opt/math-and-data-model-specifications)
defines field meanings and equations. A schema validates JSON structure;
successful validation does not establish numerical validity or acceptance as a
Task Force network case.

## Historical v0.1.0 baseline

[Schema 0.1.0](schema/bmopf/0.1.0/bmopf.schema.json) records the Task Force's
historical schema from `bmopf-resources`. Its field definitions and validation
rules are unchanged; only its `$id` identifies this versioned location.
[Provenance and contributors](docs/baseline-0.1.0.md) identify the exact source,
review history, licence, and checks. This import is not a release or a claim of
ratification. No `schema-v0.1.0` tag accompanies it.

The `version` annotation in the schema is `0.1.0`. A dataset may identify the
schema using `meta.$schema`; `meta.version` describes the dataset. The historical
schema does not define `meta.schema_version`. An immutable commit URL retrieves
a specific schema snapshot; its root `$id` supplies the canonical identity.

## Validate a case

```sh
python3 -m pip install jsonschema==4.25.1
python3 tests/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

The checks validate each schema, the small examples, rejected inputs, and exact
baseline provenance. [Examples](examples/0.1.0/README.md) are authored structural
fixtures, not accepted benchmark cases. Known dataset or specification questions
do not silently change the historical schema.

## 0.1.1

[Schema 0.1.1](schema/bmopf/0.1.1/bmopf.schema.json) renames the bus
phase-to-ground bounds to `vpg_min`/`vpg_max` after
[specification issue #51](https://github.com/distribution-system-opt/math-and-data-model-specifications/issues/51);
nothing else changes.

## v0.2.0

[Schema PR #2](https://github.com/distribution-system-opt/dsopt-schema/pull/2)
builds on 0.1.1. Its [proposal overview](docs/proposal-0.2.0.md),
[contributor record](docs/contributors.md),
[roadmap](docs/roadmap.md) and the paired
[specification PR #60](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/60)
describe it. Cross-field checks in `tests/semantics.py` apply to 0.2.0 documents
and do not redefine historical v0.1.0 validity.

### Versioning and compatibility

- A release number is MAJOR.MINOR.PATCH. A *line* is the releases sharing
  MAJOR.MINOR while MAJOR is 0 (0.2.0, 0.2.1, ...), and sharing MAJOR from 1.0.0.
- Within a line a later release only adds optional fields, optional tables and
  enum values, and corrects descriptions without changing their meaning. It never
  renames, removes or retypes a field, tightens a constraint, adds a required
  field, or changes a meaning or default. Every document valid under a release is
  therefore valid, with the same meaning, under every later release of its line.
- A new line (0.3.0 now; 2.0.0 after 1.0) may make any of those changes, and its
  CHANGELOG lists each one with a migration note.
- A document states `meta.schema_version`, the release it was written against.
  That is its only version identifier; it names no URL, so it does not depend on
  where schemas are hosted. Each schema accepts every release number of its own
  line and no other.
- A consumer reads the line from `meta.schema_version` and validates against the
  newest schema of that line it holds. A document from a later release of the line
  that uses nothing new still validates; one that does fails, and the consumer
  reports that it needs the later release.
- Each release has its own directory, `schema/bmopf/X.Y.Z/`, whose bytes never
  change after the `schema-vX.Y.Z` tag. Its `$id` is the URL of those bytes at that
  tag. Until the tag exists a proposal's bytes may still change; a producer that
  writes against an untagged proposal records its commit and digest in
  `meta.provenance`.
- Documents written before 0.2.0 carry no `meta.schema_version`. A reader
  identifies them by their `meta.$schema`, as 0.1.x defined; that rule is frozen.

### Conformance

The key words MUST, MUST NOT and SHOULD are used as in RFC 2119.

- A conforming 0.2.x document MUST be RFC 8259 JSON (no `NaN` or `Infinity`), MUST
  validate against the schema of its line, and MUST satisfy the semantic rules in
  [docs/conformance.md](docs/conformance.md#semantic-rules).
- A conforming producer MUST write conforming documents and MUST state the release
  it wrote against.
- A conforming consumer MUST reject a document that fails its line's schema, MUST
  NOT reinterpret a field's stated meaning, and MUST report, not silently drop, any
  table or field it does not model.

### Moving a 0.1.x document to 0.2.0

- Replace `meta.$schema` by `"schema_version": "0.2.0"` in `meta`.
- Rename bus `v_min`/`v_max` to `vpg_min`/`vpg_max` (0.1.0 only) and `vn_max` to
  `vng_max`.
- `vpg_*` arrays have one entry per phase terminal (0.1.x said per bus terminal):
  drop any neutral entry.
- Line `s_max` has one entry per conductor, as the specification and the 0.1.1
  linecode state (the 0.1.1 line text said per phase).
- Without `terminal_conventions`, terminal `"4"` is the neutral when the bus
  terminals are exactly `1`-`4` (0.1.x treated only `n`/`N` as neutral).
- A line names a `linecode` or gives inline matrices, not both; transformer
  records reject unknown keys.
- Generator `cost` remains accepted as the deprecated spelling of
  `energy_cost_rate`.

## Contribute

Corrections and proposals are welcome. Follow [CONTRIBUTING.md](CONTRIBUTING.md)
and the Task Force's existing review process. Proposed versions use new
directories; released directories are immutable. Only Task Force maintainers
ratify and release schemas with `schema-v*` tags.

Schema, documentation, and authored test examples use [CC BY 4.0](LICENSE).
Externally sourced network cases retain their own licences and attribution.
