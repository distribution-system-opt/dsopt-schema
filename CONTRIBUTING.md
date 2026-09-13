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

## Connecting issues, PRs, and contributors

The issue forms support discrepancies, proposed changes, and questions. Blank
issues remain available. Search existing discussions first and link related
work; a new form does not require a duplicate issue for an existing proposal.
Questions and editorial fixes do not need a modelling proposal or a full test
packet.

The PR template records purpose, review tier, versions, compatibility, evidence,
dependencies, contributions, and open questions. Ordinary changes start from
`main`. A stacked PR names its prerequisite and base branch, with an explicit
merge order; after the prerequisite merges, retarget it to `main` and check the
remaining diff. Paired normative PRs still need coordinated Task Force review.

Use commit co-author trailers for incorporated or adapted human-authored work,
with verified Git identities. PR descriptions separately credit review,
discussion, and coordination, linking the actual contribution. Preserve human
trailers in squash messages. A credit is not an assertion of endorsement or
ratification. Corrections and additional attribution are welcome.

Validation reports distinguish structure, semantic consistency, numerical
evidence, and acceptance as a Task Force network case. If a local build is not
possible, state why and link the CI result or preview instead of checking an
unperformed test. CI does not replace maintainer review or case acceptance.
