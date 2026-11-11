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

## Proposed v0.2.0

[Schema PR #2](https://github.com/distribution-system-opt/dsopt-schema/pull/2)
builds on 0.1.1 (it carries the `vpg_*` names, renames `vn_max` to `vng_max`, adds
`geo` slots for every element with a place on the map with `meta.crs`, and fixes
`meta.$schema` to the canonical `$id`).
Its [proposal overview](docs/proposal-0.2.0.md),
[contributor record](docs/contributors.md), and
[paired specification PR #39](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/39)
describe the proposed additions and review questions. Both versions receive
structural checks. Cross-field checks in `tests/semantics.py` apply to the
proposal examples and do not redefine historical v0.1.0 validity.

**Versions and identifiers.** A 0.2.0 document states `meta.$schema` equal to the
0.2.0 `$id` and `meta.schema_version` `"0.2.0"`, and the schema fixes both with
`const`. A 0.2.0 validator therefore rejects a 0.2.1 document, and each later
version (patch releases included) is its own schema directory with its own `$id`.
A 0.1.x document needs those two `meta` fields edited before it can validate as
0.2.0, and `vn_max` renamed `vng_max` where it appears. The `$id` is a URL under
`/main/`, which names the document's version but is not an immutable retrieval
location: the `schema-v0.2.0` tag, or the commit and digest a producer records in
`meta.provenance`, identifies the exact bytes.

## Contribute

Corrections and proposals are welcome. Follow [CONTRIBUTING.md](CONTRIBUTING.md)
and the Task Force's existing review process. Proposed versions use new
directories; released directories are immutable. Only Task Force maintainers
ratify and release schemas with `schema-v*` tags.

Schema, documentation, and authored test examples use [CC BY 4.0](LICENSE).
Externally sourced network cases retain their own licences and attribution.
