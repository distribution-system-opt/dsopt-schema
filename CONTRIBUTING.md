# Contributing to dsopt-schema

Corrections, questions, examples, and modelling proposals are welcome. The
[Task Force contribution guide](https://github.com/distribution-system-opt/math-and-data-model-specifications/blob/main/docs/src/contributing.md)
defines governance, modelling principles, review expectations, licensing, and
release procedures. The existing
[maintainer list](https://github.com/distribution-system-opt/math-and-data-model-specifications/blob/main/MAINTAINERS.md)
applies here; this repository does not establish a separate decision process.

## Review expectations

The guide distinguishes editorial changes, explanatory/non-normative changes,
and normative changes. Editorial fixes can proceed directly to a PR. Tests and
tooling receive ordinary review. Changes to field names, types, units, required
fields, permitted values, validation rules, or mathematics start with an issue
or discussion and require Task Force review. Link related work before opening a
new discussion.

A normative proposal needs paired schema and specification PRs. Field names,
prose, tables, worked examples, and equations must agree. Describe compatibility
and migration effects; do not treat an implementation release as approval.
The specification defines semantics; schema descriptions remain concise.

## Schema versions

Make changes on a branch from `main`. A new version belongs in
`schema/bmopf/<version>/bmopf.schema.json`, with examples and rejected cases in
matching version directories. State its version in the root `version` annotation
and versioned `$id`. Dataset metadata follows that version's declared fields:
0.1.0 does not permit `meta.schema_version`. Record changes in `CHANGELOG.md`.

An immutable commit URL retrieves an exact proposal snapshot. A versioned path
alone does not prove release or ratification. Released schema directories are
immutable; maintainers publish `schema-v*` tags after Task Force review.
Specification tags use `v*` in the specification repository. Dataset revisions
remain independent of both.

## Validation

```sh
python3 -m pip install jsonschema==4.25.1
python3 tests/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

Structural checks do not certify electrical references, dimensions, physical
parameters, feasibility, or a solver's capabilities. Record additional evidence
separately. Network-case acceptance remains a Task Force decision.

Small authored examples are preferred. Cite the source, revision, changes, and
licence of reused material. Retain contributors' attribution. Contributions use
[CC BY 4.0](LICENSE); externally sourced datasets need their own licence review.
