from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from leveria.audit import audit_script
from leveria.daily import run
from leveria.store import Store


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "data").mkdir()
        (self.root / "data/concepts_recuperes.json").write_text(json.dumps([
            {"id":"test","domaine":"fiscalite","titre":"Test","serie":"fiscalite","source_path":"content/fiscalite/test.md","recovered":True}
        ]))
        source = self.root / "content/fiscalite/test.md"; source.parent.mkdir(parents=True); source.write_text("# Test\nSource : https://legifrance.gouv.fr")
        self.store = Store(self.root)

    def tearDown(self): self.temp.cleanup()

    def test_calendar_has_two_slots_and_three_platforms(self):
        value = self.store.build_calendar(date(2026, 8, 24), 1)
        self.assertEqual(6, len(value["publications"]))
        self.assertEqual({1, 2}, {item["slot"] for item in value["publications"]})
        self.assertEqual({"tiktok", "reels", "shorts"}, {item["platform"] for item in value["publications"]})

    def test_daily_is_locked_when_scripts_are_missing(self):
        self.store.build_calendar(date(2026, 8, 24), 1)
        manifest = json.loads(run(self.store, date(2026, 8, 24), 1).read_text())
        self.assertTrue(manifest["publish_locked"])
        self.assertTrue(all(item["status"] == "blocked" for item in manifest["items"]))

    def test_audit_requires_official_source(self):
        result = audit_script("## Narration continue\n" + "mot " * 100, "tiktok")
        self.assertFalse(result.ok)
        self.assertTrue(any("source" in item.lower() for item in result.errors))


if __name__ == "__main__": unittest.main()
