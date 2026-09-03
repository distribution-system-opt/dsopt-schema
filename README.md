# dsopt-schema

The JSON Schema documents released by the IEEE PES Task Force on Benchmarking
Multiconductor OPF (BMOPF) for Distribution Systems.

This repository is the canonical home of the BMOPF data schema, as named by the
Task Force's [specification
repository](https://github.com/distribution-system-opt/math-and-data-model-specifications).
A schema here defines the structure of a BMOPF network case: the table and field
names, the types, which fields are required, and the array and matrix key
shapes. The meaning of every field, the mathematical model, and the OPF
formulation live in the specification, which is normative for semantics; a
schema is normative for structure. The two are kept in agreement, and a field
rename is not complete until both state the new name.

## Layout

```
schema/bmopf/<version>/bmopf.schema.json   one released or proposed schema version
examples/<version>/                        cases that validate against that version
tests/validate.py                          validates every example, and checks the rejections
CHANGELOG.md                               what changed between versions
```

Each version is an immutable directory. A published version is never edited in
place; a correction is a new version.

## Versioning

A schema version is `MAJOR.MINOR.PATCH` and is released as a git tag
`schema-vMAJOR.MINOR.PATCH`, the prefix the specification repository's
contributing guide reserves for schema releases so a schema tag never reads as a
specification documentation version.

A schema document states its own version twice, and a case states which one it
was written against:

- `$id` is the raw URL of the document, and carries the version.
- `meta.schema_version` is a constant equal to that version, so a case that
  states it cannot claim a version the document does not have.
- `meta.$schema` in a case is the `$id` of the schema the case validates
  against. A reader selects the schema version from this field. A case that
  omits it declares no version.

`meta.version` in a case is the version of the dataset, chosen by whoever
publishes the case. It is unrelated to the schema version: a case may revise its
own data many times against one schema version.

## Validating a case

`tests/validate.py` needs the `jsonschema` package.

```
python3 -m pip install jsonschema
python3 tests/validate.py
```

It validates every file under `examples/<version>/` against
`schema/bmopf/<version>/bmopf.schema.json`, and checks that the documents under
`tests/rejected/<version>/` are each rejected, so the strictness rules stay
enforced rather than merely described.

## What the schema rejects

Every object in a BMOPF schema sets `additionalProperties` to `false`, and the
matrix element names are the only pattern-matched keys. An unknown field is
rejected wherever it appears.

The single exception is the top-level `extras` object, which is free-form. Data
there carries no defined meaning, so a reader that ignores `extras` reads a
different network than the writer wrote. A writer that moves data into `extras`
rather than dropping it says so.

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), the same licence as
the specification; see [LICENSE](LICENSE). By opening a pull request you agree
to license your contribution under the same terms.

Network cases are licensed separately. Each inherits the licence of the data it
derives from, recorded in its own `meta.license` field, and this repository's
licence does not apply to them.

## Citation

A schema is versioned and not static. Cite the version, by its tag, that a
result was produced against.
