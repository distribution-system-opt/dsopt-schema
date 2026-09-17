"""Pin the historical schema bytes while allowing its documented relocation."""

from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parent.parent


class BaselineProvenance(unittest.TestCase):
    def test_exact_upstream_bytes_except_root_identity(self):
        provenance = json.loads((ROOT / 'provenance/0.1.0.json').read_text())
        content = (ROOT / 'schema/bmopf/0.1.0/bmopf.schema.json').read_bytes()
        schema = json.loads(content)
        self.assertEqual(schema['$id'], provenance['canonical_id'])
        self.assertEqual(content.count(provenance['canonical_id'].encode()), 1)
        upstream = content.replace(
            provenance['canonical_id'].encode(), provenance['source_id'].encode(), 1
        )
        self.assertEqual(len(upstream), 36141)
        self.assertEqual(
            hashlib.sha256(upstream).hexdigest(),
            'a74f4d2be151e4b250a47a1730445301c093572fce8de609e9af15b76c67ef73',
        )
        self.assertEqual(provenance['sha256'], hashlib.sha256(upstream).hexdigest())


if __name__ == '__main__':
    unittest.main()
