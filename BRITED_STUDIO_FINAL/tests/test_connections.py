from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from leveria.connections import PlatformConnections, REQUIRED


class MemoryVault:
    def __init__(self):
        self.values = {}

    @staticmethod
    def available():
        return True

    def set(self, platform, key, value):
        self.values[(platform, key)] = value

    def get(self, platform, key):
        return self.values.get((platform, key))


class PlatformConnectionsTests(unittest.TestCase):
    def test_reports_missing_without_leaking_secrets(self):
        with tempfile.TemporaryDirectory() as folder:
            result = PlatformConnections(Path(folder), MemoryVault()).status()
            self.assertFalse(result["all_configured"])
            self.assertTrue(result["publication_locked"])
            self.assertNotIn("access_token", str(result.get("values", {})))

    def test_saves_secrets_only_in_vault(self):
        with tempfile.TemporaryDirectory() as folder:
            vault = MemoryVault()
            service = PlatformConnections(Path(folder), vault)
            values = {key: f"secret-{key}" for key in REQUIRED["youtube"]}
            result = service.save_public_setup("youtube", values)
            youtube = next(x for x in result["platforms"] if x["platform"] == "youtube")
            self.assertTrue(youtube["configured"])
            public_file = (Path(folder) / "data/platform_connections.json").read_text()
            self.assertNotIn("secret-client_id", public_file)


if __name__ == "__main__":
    unittest.main()
