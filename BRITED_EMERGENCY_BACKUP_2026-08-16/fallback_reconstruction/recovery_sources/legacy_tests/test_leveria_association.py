"""Non-regression checks for calendar-to-script associations."""

from __future__ import annotations

import tempfile
import unittest
import json
from pathlib import Path
from unittest.mock import patch

from leveria.planning import Plan, Publication, load_plan, save_plan
from leveria.formats import REELS
from leveria.script import ScriptParseError, parse_script
from leveria.server import Handler


SCRIPT = "# Script test\n\n## Narration continue\n\nTexte.\n"


class AssociationServerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp())
        self.plan_path = self.temp / "calendrier.json"
        self.scripts_root = self.temp / "scripts"
        self.publication = Publication(
            id="2026-08-24:tiktok:regimes_communaute_par_defaut:0",
            date="2026-08-24",
            platform="tiktok",
            concept_id="regimes_communaute_par_defaut",
            titre="Se marier sans contrat, c'est déjà choisir un régime #1",
            angle_index=0,
        )
        save_plan(Plan((self.publication,)), self.plan_path)
        self.patches = (
            patch("leveria.server._plan_path", return_value=str(self.plan_path)),
            patch("leveria.server._scripts_root", return_value=str(self.scripts_root)),
        )
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)
    def post(self, payload: dict) -> tuple[int, dict]:
        handler = object.__new__(Handler)
        handler.path = "/enregistrer"
        handler._body = lambda: payload
        captured: list[tuple[int, dict]] = []
        handler._send = lambda status, result: captured.append((status, result))
        handler.do_POST()
        self.assertEqual(len(captured), 1)
        return captured[0]

    def payload(self, **changes: object) -> dict:
        value = {
            "conceptId": self.publication.concept_id,
            "format": self.publication.platform,
            "angle": 1,
            "publicationId": self.publication.id,
            "domaine": "regimes_matrimoniaux",
            "ok": True,
            "markdown": SCRIPT,
        }
        value.update(changes)
        return value

    def test_save_preserves_angle_and_links_publication(self) -> None:
        status, result = self.post(self.payload())
        self.assertEqual(status, 200)
        self.assertTrue(result["path"].endswith("__tiktok__a1.md"))
        linked = load_plan(self.plan_path).get(self.publication.id)
        self.assertEqual(linked.script_path, result["path"])
        self.assertEqual(linked.statut, "script_pret")

    def test_wrong_angle_is_rejected_before_writing(self) -> None:
        status, result = self.post(self.payload(angle=2))
        self.assertEqual(status, 409)
        self.assertIn("angle", result["error"])


class BeatOrderTests(unittest.TestCase):
    def raw(self, ids: list[tuple[str, str]]) -> str:
        return json.dumps(
            {
                "titre": "Test",
                "angle": "Test",
                "beats": [
                    {
                        "id": identifier,
                        "label": label,
                        "narration": f"Narration {label}",
                        "visuel": "Visuel",
                    }
                    for identifier, label in ids
                ],
            }
        )

    def test_instagram_order_is_accepted(self) -> None:
        order = [(beat.id, beat.label) for beat in REELS.beats]
        script = parse_script(self.raw(order), "c1", "reels", REELS)
        self.assertEqual(
            [beat.label for beat in script.beats],
            ["Hook", "Idée unique", "Preuve chiffrée", "Clôture"],
        )

    def test_instagram_reordered_beats_are_rejected(self) -> None:
        wrong = [
            ("hook", "Hook"),
            ("preuve", "Preuve chiffrée"),
            ("idee", "Idée unique"),
            ("cta", "Clôture"),
        ]
        with self.assertRaisesRegex(ScriptParseError, "ordre des beats invalide"):
            parse_script(self.raw(wrong), "c1", "reels", REELS)
        self.assertFalse(any(self.scripts_root.rglob("*.md")))

    def test_wrong_platform_is_rejected_before_writing(self) -> None:
        status, result = self.post(self.payload(format="reels"))
        self.assertEqual(status, 409)
        self.assertIn("plateforme", result["error"])

    def test_angle_can_no_longer_silently_default_to_one(self) -> None:
        status, result = self.post(self.payload(angle=None))
        self.assertEqual(status, 400)
        self.assertIn("angle", result["error"])

    def test_unvalidated_script_cannot_enter_exploitable_scripts(self) -> None:
        status, result = self.post(self.payload(ok=False))
        self.assertEqual(status, 422)
        self.assertIn("non validé", result["error"])
        self.assertFalse(any(self.scripts_root.rglob("*.md")))

    def test_failed_validation_can_never_be_saved(self) -> None:
        status, result = self.post(self.payload(ok=False))
        self.assertEqual(status, 422)
        self.assertIn("seuls les scripts", result["error"])
        self.assertFalse(any(self.scripts_root.rglob("*.md")))


if __name__ == "__main__":
    unittest.main()
