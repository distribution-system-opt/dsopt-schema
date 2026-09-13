# Historical BMOPF v0.1.0 baseline

## Source and permitted change

The source is [`draft_bmopf_schema.json`](https://github.com/distribution-system-opt/bmopf-resources/blob/f2e368470a5012dd264d1f5a2f867867fb926615/draft_schema_and_networks/draft_bmopf_schema.json),
36,141 bytes, SHA-256
`a74f4d2be151e4b250a47a1730445301c093572fce8de609e9af15b76c67ef73`.
The import changes only the root `$id`. Reversing that substitution reproduces
the source bytes exactly; `tests/test_baseline.py` checks the digest offline.
[Machine-readable provenance](../provenance/0.1.0.json) records both identities.
The schema is licensed under [CC BY 4.0](../LICENSE).

This is a historical snapshot, not a new mathematical definition or release.
The root `version` annotation is `0.1.0`; the source did not declare
`meta.schema_version`, and the import does not add it. Later field corrections
or extensions need their own version and paired specification review.

## Contributions and review history

| Contributor | Work carried into the baseline | Source |
|---|---|---|
| Matt Deakin (@deakinmt) | Initial schema and networks, matrix indexing, schema/specification alignment and review | [Initial schema](https://github.com/distribution-system-opt/bmopf-resources/commit/da67a40), [matrix indexing](https://github.com/distribution-system-opt/bmopf-resources/commit/f93bca6), [review in #16](https://github.com/distribution-system-opt/bmopf-resources/pull/16) |
| Frederik Geth (@frederikgeth) | Schema development, v0.1.0 metadata and extensions, capacitor definitions, and review-driven scope changes | [v0.1.0 conventions](https://github.com/distribution-system-opt/bmopf-resources/commit/1017e6a), [review response](https://github.com/distribution-system-opt/bmopf-resources/pull/16#issuecomment-4931251306), [alignment changes](https://github.com/distribution-system-opt/bmopf-resources/commit/0dc9609) |
| Samuel Talkington (@samtalki) | Schema port, repository organization, versioned import, provenance and structural examples | [Schema port #16](https://github.com/distribution-system-opt/bmopf-resources/pull/16), [repository location #37](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/37) |

The contribution guidance adapts Matt Deakin's
[existing guide and PR template](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/3).
The Task Force's broader documentation and review work remains credited in its
source history. Credits identify contributions, not endorsement of later proposals;
corrections or additional attribution are welcome.

## Validation and outstanding questions

The small authored examples check structural behavior: required generator
`cost`, uppercase load-model values, a scalar capacitor bank rating, and
free-form `extras` and `meta.provenance`. They are not benchmark network cases.

Historical network examples remain in `bmopf-resources`. Its ENWL example
passes structural validation but names grounded terminal `5` on a bus declaring
`a,b,c,n`; a schema import does not choose a dataset repair.

Source and objective changes remain in specification
[#36](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/36)
and resources [#21](https://github.com/distribution-system-opt/bmopf-resources/pull/21).
Terminal naming and ground roles remain in specification
[#26](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/26)
and [#27](https://github.com/distribution-system-opt/math-and-data-model-specifications/issues/27).
Those discussions do not modify this snapshot.
