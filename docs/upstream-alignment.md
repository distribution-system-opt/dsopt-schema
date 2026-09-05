# Additions to existing Task Force proposals

The PowerIO integration follows Matt Deakin's work. The specification follow-up
is based on [PR #36](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/36),
revision `b0ffdbe3584046d6a631bf4f9de1d049f0b3e01d`. Its component and objective
pages provide the definitions; the integration supplement links to them.

| Existing work | Adopted definition | Additional PowerIO work |
|---|---|---|
| Specification #36, source and generator | Per-phase `energy_cost_rate` in $/kWh | Retain deprecated `cost` as an equal-valued alias; typed source prices and IR round trips |
| Specification #36, objective | One-hour cost objective and injected-power convention | No alternative objective, KCL equation, feasibility relaxation or duration field |
| Resources [#21](https://github.com/distribution-system-opt/bmopf-resources/pull/21), `5c63506892b97cf2c0333c7ffec1a9b3e5b1b791` | New energy-price spelling | Carry it into the current schema repository; preserve older datasets through the alias |
| Specification [#26](https://github.com/distribution-system-opt/math-and-data-model-specifications/pull/26), `0bdf9715f4d12334c4a10ee0e9f5bc40fd6ebe4d` | Terminal spellings are examples, not mandatory canonical names | Preserve explicit names and metadata; document PowerIO's legacy inference separately |
| Task Force transformer and distribution work | Existing component equations and stated units | Additional equipment fields, worked examples and independently checked conversion evidence |

The source-price description in resources #21 says both "per-phase" and "one
entry per terminal". The source and objective pages in #36 consistently say
per-phase, which this integration follows. A neutral terminal therefore has no
price entry. Voltage arrays retain every source terminal. These are separate
array dimensions and both receive tests.

Terminal-role categories remain under discussion in #26 and issue #27. The
integration preserves old `terminal_conventions` metadata and documents the
reader's fallback assumptions; it does not settle a new Task Force taxonomy.
Optional IBR price data and transformer additions remain proposed extensions.
Their preservation does not change the base source/generator objective or imply
that every consumer implements their equations.

Ratification, changes requested during review, and the eventual schema tag remain
Task Force decisions. PowerIO v0.11.0 supports the identified draft; a later
compatible release can follow the reviewed result.
