from __future__ import annotations

import json
import tempfile
import unittest
from unittest.mock import patch
from datetime import date
from pathlib import Path

from leveria.charte import INTERDITS, PRESENTATION_PAR_PLATEFORME, SERIES
from leveria.daily import run
from leveria.formats import REELS, SHORTS, TIKTOK
from leveria.generator import next_version
from leveria.store import Store, editorial_diversity
from leveria.performance import score_script
from leveria.scheduler import Scheduler
from leveria.queue import ProductionQueue
from leveria.prompts import brief
from leveria.review_agents import review_script
from leveria.review_agents import AGENTS
from leveria.format_adapter import adapt_beats, beats_from_markdown, normalized
from leveria.script_batch import ScriptBatch
from leveria.compliance import check
from leveria.audit import audit_script
from leveria.cta import APPOINTMENT, EDUCATIONAL, cta_mode
from leveria.server import safe_web_target


class FinalRulesTests(unittest.TestCase):
    def test_editorial_policy_teaches_before_it_converts(self):
        policy = json.loads((Path(__file__).parents[1] / "data/editorial_policy.json").read_text(encoding="utf-8"))
        mission = policy["editorial_mission"]
        self.assertIn("Grand public", mission["audience"])
        self.assertIn("complète avant le CTA", mission["conversion_rule"])
        self.assertIn("14 jours", mission["diversity_rule"])

    def test_unexplained_technical_jargon_is_rejected(self):
        script = "## Narration continue\nVotre échange contient-il une soulte ?\nNon.\nConcrètement, elle change la fiscalité.\n## Sources\nhttps://legifrance.gouv.fr\n## Mention\nContenu pédagogique général."
        result = audit_script(script, "shorts")
        self.assertTrue(any("terme technique non expliqué" in error for error in result.errors))

    def test_four_editorial_series_are_present_in_every_fourteen_day_window(self):
        publications = []
        series = ["fiscalite", "immobilier", "juridique", "finance"]
        for offset in range(14):
            for slot in (1, 2):
                publications.append({"date": f"2026-09-{offset + 1:02d}", "slot": slot,
                                     "platform": "shorts", "serie": series[(offset + slot) % 4],
                                     "concept_id": f"topic-{offset}-{slot}"})
        self.assertTrue(editorial_diversity(publications)["passed"])

    def test_public_web_route_blocks_plain_and_encoded_traversal(self):
        self.assertIsNone(safe_web_target("/../server.py"))
        self.assertIsNone(safe_web_target("/%2e%2e/server.py"))
        self.assertIsNone(safe_web_target("/../../.env"))

    def test_final_scripts_rejects_an_invalid_date(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root / "data").mkdir()
            with self.assertRaisesRegex(ValueError, "Date invalide"):
                Store(root).final_scripts("not-a-date")

    def test_shooting_library_exposes_drafts_without_marking_them_final(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root / "data").mkdir(); (root / "content").mkdir(); (root / "scripts").mkdir(); (root / "production").mkdir()
            path = "scripts/example__shorts__a1.md"
            (root / path).write_text("## Narration continue\nImaginez que vous gagnez 1 000 €.\n## Sources\nhttps://impots.gouv.fr\n## Mention\nContenu pédagogique", encoding="utf-8")
            (root / "data/calendrier.json").write_text(json.dumps({"publications": [{"id": "draft", "date": "2026-09-02", "slot": 1, "platform": "shorts", "titre": "Brouillon", "script_path": path}]}), encoding="utf-8")
            result = Store(root).shooting_library("2026-09-02", 14)
            self.assertEqual(1, result["drafts"])
            self.assertEqual(0, result["ready"])
            self.assertEqual("draft", result["scripts"][0]["status"])

    def test_final_scripts_exposes_only_complete_current_certifications(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root / "data/reviews").mkdir(parents=True); (root / "scripts/x").mkdir(parents=True)
            (root / "data/editorial_policy.json").write_text('{"version":"grand-public"}', encoding="utf-8")
            script_path = "scripts/x/test__shorts__a1.md"
            review_path = "data/reviews/test.json"
            (root / script_path).write_text("## Narration continue\nUn texte prêt.\n## Sources\nhttps://impots.gouv.fr", encoding="utf-8")
            agents = {name: {"passed": True, "score": 10.0, "findings": [], "recommendations": []} for name in AGENTS}
            (root / review_path).write_text(json.dumps({"passed": True, "overall": 10.0, "agents": agents,
                                                       "errors": [], "recommendations": []}), encoding="utf-8")
            (root / "data/validations.json").write_text(json.dumps({script_path: {"validated": True, "score": 10.0,
                "threshold": 10.0, "review_path": review_path,
                "editorial_policy_sha256": Store(root).editorial_policy_hash()}}), encoding="utf-8")
            (root / "data/calendrier.json").write_text(json.dumps({"publications": [
                {"id": "ready", "date": "2026-09-01", "slot": 1, "platform": "shorts", "titre": "Prêt", "script_path": script_path},
                {"id": "pending", "date": "2026-09-01", "slot": 2, "platform": "shorts", "titre": "Attente", "script_path": ""}
            ]}), encoding="utf-8")
            class Audit:
                ok = True; errors = []; warnings = []
            with patch("leveria.audit.audit_script", return_value=Audit()):
                result = Store(root).final_scripts("2026-09-01")
            self.assertEqual(["ready"], [item["id"] for item in result["scripts"]])
            self.assertEqual(15, result["scripts"][0]["agents"])
            self.assertEqual(1, result["pending"])

    def test_face_camera_rejects_a_generic_course_hook(self):
        script = "## Narration continue\nAujourd'hui, nous allons voir comment fonctionne votre fiscalité.\n## Sources\nhttps://www.impots.gouv.fr\n## Mention\nContenu pédagogique général. Ne constitue pas un conseil."
        result = audit_script(script, "shorts")
        self.assertTrue(any("Hook générique ou professoral" in error for error in result.errors))

    def test_face_camera_rejects_a_hook_longer_than_eighteen_words(self):
        hook = " ".join(["attention"] * 19) + " ?"
        script = f"## Narration continue\n{hook}\n## Sources\nhttps://www.impots.gouv.fr\n## Mention\nContenu pédagogique général. Ne constitue pas un conseil."
        result = audit_script(script, "shorts")
        self.assertTrue(any("Hook trop long" in error for error in result.errors))

    def test_face_camera_rejects_teaching_transitions(self):
        script = "## Narration continue\nCombien pouvez-vous perdre ? Premièrement, il convient de regarder la règle.\n## Sources\nhttps://www.impots.gouv.fr\n## Mention\nContenu pédagogique général. Ne constitue pas un conseil."
        result = audit_script(script, "shorts")
        self.assertTrue(any("Ton de cours" in error for error in result.errors))

    def test_face_camera_requires_audience_projection_in_the_example(self):
        script = "## Narration continue\nVotre impôt augmente-t-il sur tout votre revenu ?\nNon.\nConcrètement, un revenu de 1 000 € produit 300 € d'impôt.\n## Sources\nhttps://www.impots.gouv.fr\n## Mention\nContenu pédagogique général. Ne constitue pas un conseil."
        result = audit_script(script, "shorts")
        self.assertTrue(any("ne projette pas explicitement" in error for error in result.errors))

    def test_face_camera_accepts_a_natural_audience_projection(self):
        script = "## Narration continue\nVotre impôt augmente-t-il sur tout votre revenu ?\nNon.\nImaginez que vous gagnez 1 000 € de plus : seule une partie change de taux.\n## Sources\nhttps://www.impots.gouv.fr\n## Mention\nContenu pédagogique général. Ne constitue pas un conseil."
        result = audit_script(script, "shorts")
        self.assertFalse(any("ne projette pas explicitement" in error for error in result.errors))

    def test_face_camera_requires_a_practical_takeaway_before_cta(self):
        script = "## Narration continue\nVotre impôt augmente-t-il sur tout votre revenu ?\nNon.\nImaginez que vous gagnez 1 000 € de plus : seule une partie change de taux.\nVous souhaitez faire le point sur votre situation ? Prenez rendez-vous via le lien dans ma bio.\n## Sources\nhttps://www.impots.gouv.fr\n## Mention\nContenu pédagogique général. Ne constitue pas un conseil."
        result = audit_script(script, "shorts")
        self.assertTrue(any("Valeur concrète" in error for error in result.errors))

    def test_face_camera_accepts_a_precise_practical_takeaway(self):
        script = "## Narration continue\nVotre impôt augmente-t-il sur tout votre revenu ?\nNon.\nImaginez que vous gagnez 1 000 € de plus : seule une partie change de taux. Vérifiez séparément votre tranche marginale et votre taux de prélèvement.\n## Sources\nhttps://www.impots.gouv.fr\n## Mention\nContenu pédagogique général. Ne constitue pas un conseil."
        result = audit_script(script, "shorts")
        self.assertFalse(any("Valeur concrète" in error for error in result.errors))

    def test_face_camera_rejects_two_opening_questions(self):
        script = "## Narration continue\nVotre échange de cryptos déclenche-t-il un impôt ?\nFaut-il déclarer chaque opération ?\n## Sources\nhttps://www.impots.gouv.fr\n## Mention\nContenu pédagogique général. Ne constitue pas un conseil."
        result = audit_script(script, "shorts")
        self.assertTrue(any("Valeur retardée" in error for error in result.errors))

    def test_face_camera_rejects_a_second_question_even_after_a_statement_hook(self):
        script = "## Narration continue\nVos pièces d'or peuvent coûter 11,5 % à la revente.\nQuelle taxe s'applique ?\n## Sources\nhttps://www.impots.gouv.fr\n## Mention\nContenu pédagogique général. Ne constitue pas un conseil."
        result = audit_script(script, "shorts")
        self.assertTrue(any("Valeur retardée" in error for error in result.errors))

    def test_face_camera_rejects_the_spoken_label_la_question(self):
        script = "## Narration continue\nVotre échange reste-t-il neutre fiscalement ?\nLa question : quel impôt se déclenche ?\n## Sources\nhttps://www.impots.gouv.fr\n## Mention\nContenu pédagogique général. Ne constitue pas un conseil."
        result = audit_script(script, "shorts")
        self.assertTrue(any("Libellé de fabrication" in error for error in result.errors))

    def test_face_camera_rejects_an_awkward_tax_question(self):
        script = "## Narration continue\nEst-ce que cet échange vous impose ?\nNon, il reste en sursis.\n## Sources\nhttps://www.impots.gouv.fr\n## Mention\nContenu pédagogique général. Ne constitue pas un conseil."
        result = audit_script(script, "shorts")
        self.assertTrue(any("Question orale maladroite" in error for error in result.errors))

    def test_face_camera_rejects_an_unbreathable_sentence(self):
        from leveria.audit import audit_script
        long_sentence = " ".join(["mot"] * 36) + "."
        script = "## Narration continue\n" + long_sentence + "\n## Sources\nhttps://www.impots.gouv.fr\n## Mention\nContenu pédagogique général. Ne constitue pas un conseil."
        result = audit_script(script, "shorts")
        self.assertTrue(any("souffle naturel" in error for error in result.errors))

    def test_cta_prioritizes_community(self):
        from datetime import timedelta
        start = date(2026, 8, 24)
        values = [cta_mode(start + timedelta(days=offset), slot) for offset in range(7) for slot in (1, 2)]
        self.assertEqual(8, values.count(EDUCATIONAL))
        self.assertEqual(1, values.count(APPOINTMENT))

    def test_platform_durations_are_the_last_validated_values(self):
        self.assertEqual((60, 65), (TIKTOK.target_seconds_min, TIKTOK.target_seconds_max))
        self.assertEqual((60, 65), (REELS.target_seconds_min, REELS.target_seconds_max))
        self.assertEqual((60, 65), (SHORTS.target_seconds_min, SHORTS.target_seconds_max))
        self.assertEqual(65, SHORTS.hard_maximum_seconds)
        self.assertEqual("Face caméra · script unique", SHORTS.label)

    def test_instagram_order_is_exact(self):
        self.assertEqual(["hook", "question", "reponse", "regle", "exemple", "nuance", "cta"],
                         [beat.id for beat in REELS.beats])

    def test_all_platforms_use_the_single_youtube_guidance(self):
        self.assertEqual({"tiktok", "reels", "shorts"}, set(PRESENTATION_PAR_PLATEFORME))
        self.assertEqual(1, len(set(PRESENTATION_PAR_PLATEFORME.values())))
        self.assertEqual(PRESENTATION_PAR_PLATEFORME["shorts"], PRESENTATION_PAR_PLATEFORME["tiktok"])

    def test_series_are_brown_terracotta_ochre_royal_blue(self):
        self.assertEqual(["#6F4E37", "#C96F4A", "#D99A2B", "#2457D6"],
                         [serie.couleur_secondaire for serie in SERIES])

    def test_visual_prohibitions_are_recorded(self):
        joined = " ".join(INTERDITS).casefold()
        for value in ("crayon jaune", "barre de progression en haut", "dessin coupé",
                      "pictogramme sur le texte", "nom de l'application"):
            self.assertIn(value, joined)

    def test_validated_file_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); first = root / "x__tiktok__a1.md"; first.write_text("validé")
            second = next_version(root, "x", "tiktok", 1)
            self.assertEqual("x__tiktok__a1__v2.md", second.name)
            self.assertEqual("validé", first.read_text())

    def test_daily_rejects_an_unvalidated_script(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root / "data").mkdir(); (root / "scripts/x").mkdir(parents=True)
            (root / "content/x").mkdir(parents=True)
            (root / "content/x/test.md").write_text("---\nid: test\n---\nSource https://legifrance.gouv.fr")
            (root / "scripts/x/test__tiktok__a1.md").write_text("## Narration continue\nTexte")
            (root / "data/concepts_recuperes.json").write_text(json.dumps([
                {"id":"test","domaine":"x","titre":"Test","serie":"finance","source_path":"content/x/test.md","recovered":True}
            ]))
            store = Store(root); calendar = store.build_calendar(date(2026, 8, 24), 1)
            manifest = json.loads(run(store, date(2026, 8, 24), 1).read_text())
            self.assertEqual("blocked", manifest["status"])
            youtube = next(x for x in manifest["items"] if x["platform"] == "shorts")
            self.assertEqual("blocked", youtube["status"])
            self.assertIn("Script natif validé absent", youtube["warnings"][0])

    def test_calendar_defaults_to_six_months(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root / "data").mkdir(); (root / "content/x").mkdir(parents=True)
            (root / "content/x/test.md").write_text("---\nid: test\n---\nSource https://legifrance.gouv.fr")
            (root / "data/concepts_recuperes.json").write_text(json.dumps([
                {"id":"test","domaine":"x","titre":"Test","serie":"finance","source_path":"content/x/test.md","recovered":True}
            ]))
            value = Store(root).build_calendar(date(2026, 8, 24))
            self.assertEqual(1080, len(value["publications"]))

    def test_scheduler_only_triggers_at_exact_minute(self):
        from datetime import datetime
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root / "data").mkdir()
            (root / "data/automation.json").write_text(json.dumps({"active": True, "runs": [{"slot": 1, "time": "10:00"}]}))
            scheduler = Scheduler(Store(root), lambda *_: None)
            self.assertEqual(1, scheduler.due(datetime(2026, 8, 24, 10, 0)))
            self.assertIsNone(scheduler.due(datetime(2026, 8, 24, 10, 1)))

    def test_calendar_never_schedules_an_uncertified_concept(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root / "data").mkdir(); (root / "content/x").mkdir(parents=True)
            (root / "content/x/safe.md").write_text("---\nid: safe\n---\nSource https://legifrance.gouv.fr")
            (root / "data/concepts_recuperes.json").write_text(json.dumps([
                {"id":"safe","domaine":"x","titre":"Sûr","serie":"finance","source_path":"content/x/safe.md","recovered":True},
                {"id":"missing","domaine":"x","titre":"Bloqué","serie":"finance","source_path":"","recovered":False}
            ]))
            value = Store(root).build_calendar(date(2026, 8, 24), 2)
            self.assertEqual({"safe"}, {item["concept_id"] for item in value["publications"]})

    def test_heritage_is_searchable_and_paginated(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root / "data").mkdir()
            (root / "data/history.json").write_text(json.dumps({"summary":{"conversation_messages":2},"conversation_messages":[{"text":"TikTok"},{"text":"Instagram"}],"subject_bank":[],"artifacts":[]}))
            result = Store(root).search_heritage("TikTok", "conversation", 0, 1)
            self.assertEqual(1, result["total"]); self.assertEqual("TikTok", result["items"][0]["text"])

    def test_automatic_certification_requires_every_agent_at_10(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); (root/"data/reviews").mkdir(parents=True); (root/"scripts").mkdir()
            script=root/"scripts/test.md"; script.write_text("script")
            from leveria.review_agents import AGENTS
            agents={name:{"passed":True,"score":10.0} for name in AGENTS}
            review=root/"data/reviews/test.json"; review.write_text(json.dumps({"passed":True,"agents":agents}))
            (root/"data/calendrier.json").write_text(json.dumps({"publications":[{"id":"p","date":"2026-08-24","platform":"tiktok","concept_id":"test","slot":1}]}))
            result=Store(root).auto_validate_script("scripts/test.md","p","data/reviews/test.json",10.0)
            self.assertTrue(result["validated"]); self.assertEqual("automatic_committee",result["mode"])

    def test_automatic_certification_refuses_a_low_score(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); (root/"data").mkdir(); store=Store(root)
            with self.assertRaisesRegex(ValueError,"10/10"):
                store.auto_validate_script("missing.md","p","missing.json",9.9)

    def test_review_fails_closed_without_review_service(self):
        import os
        from leveria.local_llm import LocalAIUnavailable
        previous=os.environ.pop("OPENAI_API_KEY",None)
        try:
            with tempfile.TemporaryDirectory() as folder:
                root=Path(folder); (root/"data").mkdir()
                with patch("leveria.review_agents.call_local", side_effect=LocalAIUnavailable("test")):
                    result=review_script("Source", "Script", "tiktok", root=root)
            self.assertFalse(result.passed)
            self.assertTrue(any("zéro token" in item for item in result.errors))
        finally:
            if previous is not None: os.environ["OPENAI_API_KEY"]=previous

    def test_production_day_exposes_all_six_scripts_and_reviews(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); (root/"data").mkdir(); (root/"content/x").mkdir(parents=True); (root/"scripts/x").mkdir(parents=True)
            (root/"content/x/test.md").write_text("---\nid: test\n---\nSource https://legifrance.gouv.fr")
            (root/"data/concepts_recuperes.json").write_text(json.dumps([{"id":"test","domaine":"x","titre":"Test","serie":"finance","source_path":"content/x/test.md","recovered":True}]))
            store=Store(root); value=store.build_calendar(date(2026,8,24),1)
            for item in value["publications"]:
                path=root/f"scripts/x/{item['platform']}.md"; path.write_text("# Script complet")
                store.update_publication(item["id"],script_path=str(path.relative_to(root)))
            result=store.production_day("2026-08-24")
            self.assertEqual(6,result["summary"]["total"]); self.assertEqual(1,result["summary"]["scripts"])
            self.assertTrue(all("Script complet" in item["script_text"] for item in result["publications"]))

    def test_editorial_policy_is_injected_in_generation_brief(self):
        text = brief("tiktok", "Titre", "id", "Source", {"publication":{"times":["10:00","17:00"]}})
        self.assertIn("POLITIQUE ÉDITORIALE VALIDÉE", text)
        self.assertIn('"10:00"', text)

    def test_production_queue_persists_failures_and_allows_retry(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); (root/"data").mkdir()
            def broken(*args, **kwargs): raise RuntimeError("test failure")
            queue=ProductionQueue(Store(root), broken)
            job=queue.enqueue(date(2026,8,24),1); queue.run_pending()
            saved=queue.load()["jobs"][0]
            self.assertEqual("failed",saved["status"]); self.assertEqual(1,saved["attempts"])
            queue.retry(job["id"])
            self.assertEqual("queued",queue.load()["jobs"][0]["status"])

    def test_local_backup_contains_editorial_state(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); (root/"data").mkdir(); (root/"scripts").mkdir()
            (root/"data/calendrier.json").write_text('{"publications": []}')
            (root/"scripts/example.md").write_text("script")
            result=Store(root).backup("test")
            snapshot=root/result["path"]
            self.assertTrue((snapshot/"data/calendrier.json").is_file())
            self.assertTrue((snapshot/"scripts/example.md").is_file())
            self.assertTrue((snapshot/"backup.json").is_file())

    def test_rebuilding_calendar_archives_previous_version(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); (root/"data").mkdir(); (root/"content/x").mkdir(parents=True)
            (root/"content/x/test.md").write_text("---\nid: test\n---\nSource https://legifrance.gouv.fr")
            (root/"data/concepts_recuperes.json").write_text(json.dumps([
                {"id":"test","domaine":"x","titre":"Test","serie":"finance","source_path":"content/x/test.md","recovered":True}
            ]))
            store=Store(root); store.build_calendar(date(2026,8,24),1); store.build_calendar(date(2026,9,1),1)
            self.assertEqual(1,len(list((root/"recovery/calendar_versions").glob("calendrier-*.json"))))

    def test_format_agent_keeps_one_coherent_beat_on_one_page_without_changing_words(self):
        text = " ".join(f"mot{i}" for i in range(55)) + "."
        source = [{"id":"regle","narration":text,"visual":"schéma","screen_text":""}]
        pages, report = adapt_beats(source, "tiktok")
        self.assertEqual(len(pages), 1)
        self.assertTrue(report.passed)
        self.assertEqual(normalized(text), normalized(" ".join(page["narration"] for page in pages)))
        self.assertGreaterEqual(report.minimum_font_size, 32)

    def test_format_agent_keeps_question_and_answer_roles(self):
        source = [
            {"id":"question","narration":"Selon vous cette somme reste-t-elle personnelle après le mariage oui ou non ?","visual":"","screen_text":""},
            {"id":"reponse","narration":"Non, pas nécessairement.","visual":"","screen_text":""},
        ]
        pages, report = adapt_beats(source, "tiktok")
        self.assertTrue(report.exact_text_preserved)
        self.assertEqual("question", pages[0]["page_role"])
        self.assertEqual("reponse", pages[-1]["page_role"])

    def test_format_agent_preserves_approved_cta(self):
        source = [{
            "id": "cta",
            "narration": "Vous souhaitez faire le point ? Prenez rendez-vous via le lien sur mon profil.",
            "visual": "calendrier",
            "screen_text": "profil",
        }]
        pages, report = adapt_beats(source, "shorts")
        self.assertTrue(report.passed)
        self.assertFalse(report.cta_normalized)
        self.assertTrue(report.exact_text_preserved)
        self.assertEqual(
            source[0]["narration"],
            pages[0]["narration"],
        )

    def test_question_choices_are_removed_even_before_a_question_mark(self):
        markdown = "| 1 | Question | Selon vous, ce régime s'applique-t-il, oui ou non ? | choix | question |"
        beats = beats_from_markdown(markdown)
        self.assertEqual("Selon vous, ce régime s'applique-t-il", beats[0]["narration"])

    def test_whisper_acquets_homophone_is_normalized_strictly(self):
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "video_pipeline"))
        from verify_voice_content import normalize
        self.assertEqual(normalize("acquêts"), normalize("aquais"))

    def test_script_batch_state_is_resumable(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); (root/"data").mkdir(); store=Store(root); batch=ScriptBatch(store)
            batch.save({"status":"running","items":[
                {"publication_id":"done","status":"certified"},
                {"publication_id":"wait","status":"pending"},
                {"publication_id":"bad","status":"blocked"},
            ]})
            state=batch.load()
            self.assertEqual("pending",state["items"][1]["status"])
            self.assertEqual("blocked",state["items"][2]["status"])

    def test_precise_legal_citations_are_official_sources(self):
        result = check("## Sources\n- Code civil, article 515-1\n- CGI, article 796-0 bis")
        self.assertTrue(result.ok)

    def test_vague_source_label_is_not_an_official_source(self):
        result = check("## Sources\n- Un article trouvé en ligne")
        self.assertFalse(result.ok)

    def test_accented_reponse_beat_is_recognized(self):
        rows = [
            ("Hook", "Vous avez une question ?"), ("Question", "OUI ou NON ?"),
            ("Réponse", "Non."), ("Règle", "Voici la règle avec 100 euros."),
            ("Exemple", "Exemple : 100 euros."), ("Nuance", "Cela dépend du cas."),
            ("CTA", "Commentez et abonnez-vous."),
        ]
        table = "\n".join(f"| {i} | {beat} | {value} | visuel | écran |" for i, (beat, value) in enumerate(rows, 1))
        narration = " ".join(value for _, value in rows)
        text = f"| # | Beat | Narration | Visuel | Texte écran |\n{table}\n## Narration continue\n{narration}\n## Sources\nhttps://legifrance.gouv.fr\n## Mention\nContenu pédagogique"
        errors = audit_script(text, "tiktok").errors
        self.assertFalse(any("Beat obligatoire" in error for error in errors))

    def test_table_and_continuous_narration_must_match(self):
        text = "| # | Beat | Narration | Visuel | Texte écran |\n| 1 | Hook | Texte du tableau. | v | e |\n## Narration continue\nAutre texte.\n## Sources\nhttps://legifrance.gouv.fr\n## Mention\nContenu pédagogique"
        self.assertIn("Narration continue différente de la concaténation des beats", audit_script(text, "tiktok").errors)

    def test_internal_brand_names_are_forbidden_in_public_content(self):
        self.assertFalse(check("#Levéria\nhttps://legifrance.gouv.fr").ok)

    def test_obsolete_certification_is_invalidated_without_deleting_history(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); (root/"data").mkdir(); (root/"scripts/x").mkdir(parents=True)
            path="scripts/x/test__tiktok__a1.md"; (root/path).write_text("Texte non conforme")
            (root/"data/validations.json").write_text(json.dumps({path:{"validated":True,"score":10}}))
            (root/"data/calendrier.json").write_text(json.dumps({"publications":[{"id":"p","platform":"tiktok","script_path":path,"statut":"script_certifie_auto"}]}))
            result=Store(root).reconcile_certifications(); record=json.loads((root/"data/validations.json").read_text())[path]
            self.assertEqual(1,result["invalidated"]); self.assertFalse(record["validated"])
            self.assertTrue(record["previous_validation"]); self.assertTrue(record["stale"])

    def test_pilot_manifest_does_not_overwrite_daily_manifest(self):
        import inspect
        source = inspect.getsource(run)
        self.assertIn("manifest{suffix}.json", source)
        self.assertIn("platforms: list[str] | None", source)

    def test_store_reads_isolated_pilot_manifest(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); (root/"data").mkdir(); target=root/"production/2026-08-24/slot-1/manifest-pilot-reels.json"
            target.parent.mkdir(parents=True); target.write_text(json.dumps({"items": []}))
            value=Store(root).manifest("production/2026-08-24/slot-1/manifest-pilot-reels.json")
            self.assertEqual([], value["items"])

    def test_spoken_comparison_operator_is_rejected(self):
        text = "## Narration continue\nLes primes <= 150 000 euros.\n## Sources\nhttps://impots.gouv.fr"
        self.assertTrue(any("opérateurs" in error for error in audit_script(text, "shorts").errors))

    def test_assurance_vie_allowance_requires_couple_and_capital_gain_distinction(self):
        text = "## Narration continue\nAprès huit ans, l'assurance-vie bénéficie d'un abattement de quatre mille six cents euros.\n## Sources\nhttps://impots.gouv.fr"
        errors = audit_script(text, "shorts").errors
        self.assertTrue(any("9 200" in error for error in errors))
        self.assertTrue(any("capital et gains" in error for error in errors))



if __name__ == "__main__":
    unittest.main()
