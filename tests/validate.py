#!/usr/bin/env python3
"""Validate versioned schemas, structural examples, and rejected inputs."""

from pathlib import Path
import json
import sys

import jsonschema

ROOT = Path(__file__).resolve().parent.parent


def strict_json(text: str):
    """Parse RFC 8259 JSON: NaN, Infinity and -Infinity are not JSON numbers."""
    def reject(token):
        raise ValueError(f'non-finite number {token} is not JSON')
    return json.loads(text, parse_constant=reject)


def check_version(directory: Path) -> list[str]:
    version = directory.name
    schema = json.loads((directory / 'bmopf.schema.json').read_text())
    validator_class = jsonschema.validators.validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema)
    failures = []
    released_on_main = version in ('0.1.0', '0.1.1')
    expected_id = (
        'https://raw.githubusercontent.com/distribution-system-opt/dsopt-schema/'
        + ('main' if released_on_main else f'schema-v{version}')
        + f'/schema/bmopf/{version}/bmopf.schema.json'
    )
    if schema.get('$id') != expected_id:
        failures.append(f'{version}: $id disagrees with directory')
    if released_on_main and schema.get('version') != version:
        failures.append(f'{version}: version keyword disagrees with directory')
    metadata = schema.get('properties', {}).get('meta', {}).get('properties', {})
    if not released_on_main:
        line = '.'.join(version.split('.')[:2])
        accepts = jsonschema.Draft202012Validator(metadata.get('schema_version', {})).is_valid
        major, minor, _ = (int(x) for x in version.split('.'))
        if not (accepts(version) and accepts(f'{line}.7') and not accepts(f'{major}.{minor + 1}.0')):
            failures.append(f'{version}: meta.schema_version must accept the {line} line and only it')
    for folder, expected in [('examples', True), ('tests/rejected', False)]:
        cases = sorted((ROOT / folder / version).glob('*.json'))
        if not cases:
            failures.append(f'{folder}/{version}: no cases found')
        for case in cases:
            errors = list(validator.iter_errors(strict_json(case.read_text())))
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
