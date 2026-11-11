# Examples for schema 0.2.0

Illustrative cases that validate against
`schema/bmopf/0.2.0/bmopf.schema.json`. They are not benchmark network cases,
and comparing them against the feeders they are named after will not agree.

`tests/validate.py` validates every file here.

## example_features.json

A four-wire feeder written for this repository, exercising every table 0.2.0
adds: `ibr` with a converter coupled to a DC node, `control_profile` with
Volt-VAr and Volt-Watt laws, `wire_data` and `line_geometry` compiled into a
linecode, the `single_phase_autotransformer`, `open_delta_regulator` and
`n_winding` transformer subtypes, the transformer tap, winding neutral and
no-load fields, `dc_bus`, `dc_branch`, `dc_grounding`, `dc_load`, `dc_source`,
and `time_series` with and without a time axis.

Licence: CC BY 4.0, this repository's licence.

## example_enwl_n1_f2.json

Vendored from
[`distribution-system-opt/bmopf-resources`](https://github.com/distribution-system-opt/bmopf-resources)
at commit `f2e368470a5012dd264d1f5a2f867867fb926615`, directory
`draft_schema_and_networks/network_examples/` (original sha256
`24d2c054b70b5e09d179f785cb09ff90cddbf73c859756154e9eb604782b69f1`), with two
edits: `meta.$schema` now states the 0.2.0 `$id` (the original identifier is kept
as `meta.provenance.historical_schema_identifier`), and
`meta.provenance.powerio_source` is a path relative to the BMOPFTools.jl
repository instead of a local absolute path. The sha256 of the file here is
recorded in `contracts/historical.json`.

It is a 0.1.0 case, kept here to check that 0.2.0 accepts existing 0.1.0 data
once its `meta.$schema` (and `schema_version`, where present) states 0.2.0. A
0.1.x file needs that edit to validate as 0.2.0; nothing else in this case
changes.

The data derives from the four-wire low voltage network dataset:
Heidarihaei, Rahmatollah; Geth, Frederik; and Claeys, Sander (2024), v1, CSIRO
Data Collection, <https://doi.org/10.25919/jaae-vc35>, released under the
Creative Commons Attribution 4.0 International licence. The derivative carries
the same licence.

## What is not vendored here

`example_ieee13.json` from the same commit also validates against 0.2.0, but it
derives from the IEEE 13 node test feeder as distributed with OpenDSS and
carries that distribution's licence, not CC BY 4.0. It is not vendored into this
repository so every file here stays under one licence. `bmopf-resources` records
that the Task Force may replace that example.
