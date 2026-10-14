# Structural example for BMOPF 0.1.1

`small_case.json` is an authored, single-phase source/load example with a WYE
generator and a single-phase capacitor. It exercises historical field names and
types, including generator `cost`, uppercase `CONSTANT_POWER`, and scalar
capacitor `q_rated`. The example retains arbitrary metadata under `provenance`
and `extras`, including a null-valued provenance note. Those extension objects
do not impose electrical-field restrictions on their contents.

The example is identical to the case for 0.1.0 except that the schema has been
updated to 0.1.1.

The example is licensed CC BY 4.0 under the repository licence. It is a
structural fixture, not a solved or Task Force-accepted benchmark network.

