# Contributions behind the BMOPF v0.2.0 proposal

This proposal builds on the IEEE PES BMOPF Task Force's shared schema,
mathematical specification, examples and review work. Findings from developing
a reference implementation in PowerIO v0.11.0 add compatibility and numerical
evidence to that work. The proposed version and its modelling choices remain
subject to Task Force approval.

## History covered

The public repositories have no `schema-v0.1.0` release tag. The comparison starts
with Frederik Geth's [10 July 2026 commit identifying schema v0.1.0](https://github.com/distribution-system-opt/bmopf-resources/commit/1017e6aebc1307b5c96c3e0d5dea67fb8d5b8b91),
then follows the schema and specification histories, including merged changes
and the open proposals listed below, through 5 September 2026. Earlier
foundational work is credited where later changes reuse it. The specification
PDF's version is separate from the JSON Schema version.

The source history identifies six human contributors across these repositories.
Different Git names for the same person are combined here; automated
publication commits are excluded. Commit records capture only part of the Task
Force's discussion and review, so this is not an exhaustive list of everyone
who has helped develop BMOPF.

| Contributor | Recorded contribution | Source evidence |
|---|---|---|
| Frederik Geth (@frederikgeth) | Schema development and v0.1.0 metadata/extension conventions; sequence bounds, capacitor definitions and review-driven scope changes; publication of the mathematical and data specification | [v0.1.0 conventions](https://github.com/distribution-system-opt/bmopf-resources/commit/1017e6aebc1307b5c96c3e0d5dea67fb8d5b8b91), [schema revisions in #16](https://github.com/distribution-system-opt/bmopf-resources/pull/16), [specification foundation](https://github.com/distribution-system-opt/math-and-data-model-specifications/commit/10d2491bf59c482a9579fcf73a2580ce3515bf5c) |
| Matt Deakin (@deakinmt) | Schema/specification alignment, capacitor and transformer conventions, contribution guidance, component and notation clarifications; current source, KCL, objective and energy-price proposals | [capacitor/transformer #2](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/2), [guidance #3](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/3), [source/objective #36](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/36), [schema #21](https://github.com/distribution-system-opt/bmopf-resources/pull/21), [terminal naming #26](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/26) |
| Marta Vanin (@MartaVanin) | Overview and scope revisions, notation and bus clarifications, generator-cost schema consistency; workshop examples explaining conductor, grounding and network-model fidelity | [overview #11](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/11), [scope #12](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/12), [notation #13](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/13), [bus #14](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/14), [generator #16](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/16), [workshop #19](https://github.com/distribution-system-opt/bmopf-resources/pull/19) |
| Tomislav Antic (@tomislavantic) | Distribution-network scope wording and clarification of the currency/time units in energy prices | [scope #18](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/18), [units #19](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/19) |
| Naeem Turner-Bandele (@naeem627) | Review and merge coordination for the overview, scope and glossary updates | [overview #23](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/23), [scope #24](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/24), [glossary #28](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/28) |
| Samuel Talkington (@samtalki) | Schema porting and repository/versioning organization; the current versioned proposal, worked examples, compatibility tests and findings from the PowerIO reference implementation | [schema port #16](https://github.com/distribution-system-opt/bmopf-resources/pull/16), [schema repository #37](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/37), [versioned schema proposal #2](https://github.com/distribution-system-opt/dsopt-schema/pull/2), [paired supplement #39](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/39) |

## How the proposal uses that work

- The existing schema and component definitions remain the foundation. The
  historical examples retain their source content and attribution.
- The specification supplement is based on Matt's source/objective branch;
  source currents, signs, energy-price ordering and objective definitions stay
  in his component pages. Terminal-role questions remain in the existing
  discussion.
- Equipment fields set aside during v0.1.0 development are reconsidered as
  proposals. Their presence in an earlier draft does not establish acceptance
  for v0.2.0.
- Compatibility and numerical findings distinguish data preservation from
  supported calculations. A release of a reference implementation does not
  ratify the schema or prescribe the Task Force's release schedule.

The linked commits preserve their original author and co-author records.
These acknowledgments describe recorded contributions; new modelling choices
remain open for review. Corrections and additional attribution are welcome.
