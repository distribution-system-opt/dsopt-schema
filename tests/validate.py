#!/usr/bin/env python3
"""Validate versioned schemas, structural examples, and rejected inputs."""

from pathlib import Path
import json
import sys

import jsonschema

ROOT = Path(__file__).resolve().parent.parent


def check_version(directory: Path) -> list[str]:
    version = directory.name
    schema = json.loads((directory / 'bmopf.schema.json').read_text())
    validator_class = jsonschema.validators.validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema)
    failures = []
    expected_id = (
        'https://raw.githubusercontent.com/distribution-system-opt/dsopt-schema/'
        f'main/schema/bmopf/{version}/bmopf.schema.json'
    )
    if schema.get('$id') != expected_id or schema.get('version') != version:
        failures.append(f'{version}: schema identity or version disagrees with directory')
    metadata = schema.get('properties', {}).get('meta', {}).get('properties', {})
    if 'schema_version' in metadata and metadata['schema_version'].get('const') != version:
        failures.append(f'{version}: meta.schema_version disagrees with directory')
    for folder, expected in [('examples', True), ('tests/rejected', False)]:
        cases = sorted((ROOT / folder / version).glob('*.json'))
        if not cases:
            failures.append(f'{folder}/{version}: no cases found')
        for case in cases:
            errors = list(validator.iter_errors(json.loads(case.read_text())))
            label = str(case.relative_to(ROOT))
            if (not errors) != expected:
                failures.append(f'{label}: expected structural {"acceptance" if expected else "rejection"}')
                for error in errors[:5]:
                    print(f'     {list(error.absolute_path)}: {error.message}')
            else:
                print(f'ok   {label}: {"accepted" if expected else "rejected"}')
    return failures


def main() -> int:
    versions = sorted(p for p in (ROOT / 'schema/bmopf').iterdir() if p.is_dir())
    failures = [] if versions else ['No schema versions found']
    for directory in versions:
        failures.extend(check_version(directory))
    for failure in failures:
        print('FAIL ' + failure)
    return bool(failures)


if __name__ == '__main__':
    sys.exit(main())
