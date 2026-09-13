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

## Contribute

Corrections and proposals are welcome. Follow [CONTRIBUTING.md](CONTRIBUTING.md)
and the Task Force's existing review process. Proposed versions use new
directories; released directories are immutable. Only Task Force maintainers
ratify and release schemas with `schema-v*` tags.

Schema, documentation, and authored test examples use [CC BY 4.0](LICENSE).
Externally sourced network cases retain their own licences and attribution.
