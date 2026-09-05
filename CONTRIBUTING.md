# Contributing to dsopt-schema

Corrections, clarifications, and modelling proposals are welcome. Anyone may
open an issue or a pull request; maintainers from the IEEE PES Task Force on
Benchmarking Multiconductor OPF review and merge. The maintainer list is the one
in the [specification
repository](https://github.com/distribution-system-opt/math-and-data-model-specifications/blob/main/MAINTAINERS.md).

## The schema is structure, the specification is meaning

A schema document here states the structure of a BMOPF network case: table and
field names, types, required fields, enumerated values, and the array and matrix
key shapes. The [specification
site](https://distribution-system-opt.github.io/math-and-data-model-specifications)
states what every field means and what mathematics it enters. A `description` in
a schema says enough to use the field correctly and does not restate the
specification.

The two must agree. The field names in the specification prose are normative, so
a rename is not complete until the prose, the tables, the worked example, and
the schema all state the new name.

## Review tiers

The same three tiers the specification repository uses.

1. **Editorial.** Typo fixes, wording, formatting, a clearer `description` that
   preserves the meaning, and new examples that exercise only fields the schema
   already defines. Open a pull request directly.
2. **Non-normative.** Restructuring, added tests, added tooling, and a new
   example directory for an existing version. Standard review.
3. **Normative.** Any change to a field name, type, unit, optionality, meaning,
   required set, or enumerated value; any new or removed table or subtype; any
   change to the strictness rules. This needs Task Force review and starts as an
   issue or discussion, not a pull request, because agreeing it takes time. A
   normative change moves the schema version, and a proposal for one lands as a
   new version directory rather than an edit to a published version.

A normative pull request states its motivation, its effect on existing datasets,
and, where a field or value is renamed or removed, a migration note.

## Adding a version

A published version directory is immutable. To propose one:

1. Copy the previous version to `schema/bmopf/<new version>/bmopf.schema.json`
   and edit that copy.
2. Set `$id` to the raw URL of the new file and `meta.schema_version`'s `const`
   to the new version. Both carry the version, and they must agree.
3. Add `examples/<new version>/` cases exercising every field the version adds,
   and `tests/rejected/<new version>/` documents for each rejection rule the
   version introduces.
4. Record the change in `CHANGELOG.md`, naming every added, removed, and
   retyped field.
5. Run the checks below.

A maintainer releases the version by tagging `schema-v<new version>` once the
Task Force has ratified it.

## Checks

```
python3 -m pip install jsonschema
python3 tests/validate.py
```

The script checks that every schema document is itself a valid JSON Schema, that
its `$id` and `meta.schema_version` agree with its directory, that every example
validates, and that every document under `tests/rejected/` is rejected. A new
strictness rule without a rejected document is a rule nothing enforces.

## Rules the schema keeps

- **SI and absolute.** Volts, amperes, watts, vars, volt-amperes, ohms,
  siemens, metres, radians, hertz, degrees Celsius. Cost rate in currency per
  kilowatt-hour is the one deliberate exception. No per-unit quantity, and no
  unit field.
- **A complex quantity is a pair of real fields.** Rectangular or polar, as the
  element states.
- **A matrix is row first with a one-based underscore key.** Entry `A_kj` is the
  field `A_k_j`.
- **A vector is a JSON array** whose order and length are stated by the field,
  against the element's own terminal map.
- **Absence follows the field contract.** An absent bound imposes no constraint.
  Parameters use their documented defaults; for example, an omitted tap ratio
  is one, while an omitted internal neutral branch adds no grounding branch.
- **Unknown fields are rejected** except in top-level `extras` and
  `meta.provenance`, which preserve extension data and producer metadata.
- **No null anywhere.** A field a case cannot state is omitted, not nulled.

## Licence

By opening a pull request you agree to license your contribution under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), the licence of this
repository.
