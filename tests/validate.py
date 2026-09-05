#!/usr/bin/env python3
"""Check every schema version, its examples, and its rejections.

For each `schema/bmopf/<version>/bmopf.schema.json`:

- the document is itself a valid JSON Schema;
- its `$id` and its `meta.schema_version` constant both name `<version>`;
- every case under `examples/<version>/` validates against it;
- every document under `tests/rejected/<version>/` is rejected by it, so a
  strictness rule is enforced rather than only described.

Needs the `jsonschema` package. Exits nonzero on the first failure it finds,
after reporting every failure.
"""

from __future__ import annotations

import json
import sys
from semantics import validate as validate_semantics
from pathlib import Path

try:
    import jsonschema
except ModuleNotFoundError:
    sys.exit("this check needs the jsonschema package: pip install jsonschema")

ROOT = Path(__file__).resolve().parent.parent
failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)
    print("FAIL " + message)


def check_version(directory: Path) -> None:
    version = directory.name
    schema_file = directory / "bmopf.schema.json"
    schema = json.loads(schema_file.read_text())

    validator_class = jsonschema.validators.validator_for(schema)
    try:
        validator_class.check_schema(schema)
    except jsonschema.exceptions.SchemaError as error:
        fail(f"{schema_file.relative_to(ROOT)} is not a valid JSON Schema: {error}")
        return
    validator = validator_class(schema)

    expected_id = (
        "https://raw.githubusercontent.com/distribution-system-opt/dsopt-schema/"
        f"main/schema/bmopf/{version}/bmopf.schema.json"
    )
    if schema.get("$id") != expected_id:
        fail(f"{version}: $id is {schema.get('$id')!r}, expected {expected_id!r}")
    if schema.get("version") != version:
        fail(f"{version}: schema version annotation disagrees with directory")
    stated = schema["properties"]["meta"]["properties"]["schema_version"].get("const")
    if stated != version:
        fail(f"{version}: meta.schema_version const is {stated!r}")

    examples = sorted((ROOT / "examples" / version).glob("*.json"))
    if not examples:
        fail(f"{version}: no example case to validate")
    for case in examples:
        errors = sorted(
            validator.iter_errors(json.loads(case.read_text())),
            key=lambda error: list(error.absolute_path),
        )
        if errors:
            fail(f"{case.relative_to(ROOT)} does not validate")
            for error in errors[:8]:
                location = "/".join(str(part) for part in error.absolute_path)
                print(f"     {location or '<root>'}: {error.message}")
        else:
            print(f"ok   {case.relative_to(ROOT)} validates structurally")
            semantic = [[finding.code, finding.path] for finding in validate_semantics(json.loads(case.read_text()))]
            historical = json.loads((ROOT / "contracts/historical.json").read_text())
            expected = historical.get(str(case.relative_to(ROOT)), {}).get("findings", [])
            if semantic != expected:
                fail(f"{case.relative_to(ROOT)} has unexpected semantic findings: {semantic}")
            elif semantic:
                print(f"     recorded historical findings: {semantic}")

    rejected = sorted((ROOT / "tests" / "rejected" / version).glob("*.json"))
    if not rejected:
        fail(f"{version}: no rejected document, so no rejection rule is checked")
    for case in rejected:
        if validator.is_valid(json.loads(case.read_text())):
            fail(f"{case.relative_to(ROOT)} was accepted and must be rejected")
        else:
            print(f"ok   {case.relative_to(ROOT)} is rejected")


versions = sorted(path for path in (ROOT / "schema" / "bmopf").iterdir() if path.is_dir())
if not versions:
    sys.exit("no schema version found under schema/bmopf/")
for directory in versions:
    print(f"== schema/bmopf/{directory.name}")
    check_version(directory)

if failures:
    print(f"\n{len(failures)} failure(s)")
    sys.exit(1)
print("\nall checks passed")
