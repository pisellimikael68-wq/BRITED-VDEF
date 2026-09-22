from __future__ import annotations

import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from leveria.daily import _clean_script, _spec, publications_for_slot
from leveria.formats import get_format
from leveria.planning import Plan, Publication
from leveria.script import Script, ScriptBeat


class TestDailySlots(unittest.TestCase):
    def setUp(self):
        pubs=[]
        for rank,concept in enumerate(("premier","second")):
            for platform in ("shorts","reels","tiktok"):
                pubs.append(Publication(id=f"{concept}-{platform}",date="2026-08-24",platform=platform,concept_id=concept,titre=concept,rang_pedagogique=rank))
        self.plan=Plan(tuple(pubs))

    def test_first_slot_contains_first_subject_on_three_platforms(self):
        result=publications_for_slot(self.plan,date(2026,8,24),1)
        self.assertEqual({p.concept_id for p in result},{"premier"})
        self.assertEqual([p.platform for p in result],["tiktok","reels","shorts"])

    def test_second_slot_contains_second_subject(self):
        result=publications_for_slot(self.plan,date(2026,8,24),2)
        self.assertEqual({p.concept_id for p in result},{"second"})


class TestVideoSpec(unittest.TestCase):
    def test_question_answer_and_cta_are_preserved(self):
        script=Script(concept_id="x",format_id="reels",titre="Titre",angle="a",domaine="regimes_matrimoniaux",beats=(
            ScriptBeat("question","Question","Est-ce personnel ?","oui non","OUI OU NON ?"),
            ScriptBeat("reponse","Réponse","Non, pas forcément.","réponse","Non, pas forcément."),
            ScriptBeat("cta","Clôture","Enregistrez et abonnez-vous.","actions",""),
        ))
        publication=Publication(id="p",date="2026-08-24",platform="reels",concept_id="x",titre="Titre")
        spec=_spec(script,publication)
        self.assertEqual([b["id"] for b in spec["beats"]],["question","reponse","cta"])
        self.assertEqual(spec["serie"],"juridique")

    def test_an_old_structure_is_not_rendered_as_the_current_format(self):
        publication=Publication(id="p",date="2026-08-24",platform="tiktok",concept_id="x",titre="Titre")
        old=Script(concept_id="x",format_id="tiktok",titre="Titre",angle="a",domaine="d",beats=(
            ScriptBeat("hook","Hook","Un hook.","v","t"),
            ScriptBeat("regle","Règle","Une règle.","v","t"),
        ))
        with TemporaryDirectory() as folder:
            path=Path(folder)/"d"/"x__tiktok__a1.md";path.parent.mkdir()
            path.write_text(old.to_markdown(get_format("tiktok")),encoding="utf-8")
            self.assertIsNone(_clean_script(publication,"d",Path(folder)))


if __name__ == "__main__": unittest.main()
