# Roadmap after 0.2.0

The [versioning policy](../README.md#versioning-and-compatibility) sets the
boundary: a 0.2.x release only adds, so a valid 0.2.0 document stays valid with
the same meaning; anything that renames, removes, retypes, tightens or changes a
meaning waits for 0.3.0. Each item below says which side it falls on and why.

## 0.2.x: additive, planned

- **OPF formulations for the 0.2.0 tables that have none yet:** inverters and
  control profiles, the DC network, line construction (`wire_data`,
  `line_geometry`), and transformer tap and no-load-shunt equations. 0.2.0 fixes
  what each field means; these pages say how an OPF uses them. Adding equations
  for data whose meaning is already fixed changes no document.
- **Multi-period data:** ramp limits, storage state of charge and similar coupling
  between `time_series` steps, as new optional fields. 0.2.0 states that steps are
  independent snapshots, so a document without the new fields keeps that meaning.
- **Schema verification:**
  - run the cases under a second validator (for example ajv and the Rust
    `jsonschema` crate) to catch validator-specific behaviour;
  - a compatibility test that each 0.2.x schema accepts every case an earlier 0.2.x
    accepted;
  - property-based tests generating documents from the schema;
  - a digest pin of the released bytes in CI.
- **Example coverage:** examples that exercise every field, including
  `power_factor`, cable wire kinds, ZIP and exponential loads and DC droop, and a
  semantically clean ENWL case.
- **Editor support:** a SchemaStore catalog entry, so editors find the schema
  without a field in the document.

## 0.3.0: breaking, only if needed

- **Compressed or normalised representations** (Frederik, on specification #39):
  a different document structure.
- **Anything the Task Force decides differently** among the items listed as open
  in PR #2 after the tag. Each of those is a rename, a unit change or a new
  constraint, so changing it after 0.2.0 is breaking. The aim is to settle all of
  them before the tag, so that no 0.3.0 is foreseen.
