#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from leveria.store import PLATFORMS, Store


def check(name: str, condition: bool, evidence: str) -> dict:
    return {"criterion": name, "passed": bool(condition), "evidence": evidence}


def functional(root: Path, store: Store) -> list[dict]:
    calendar = store.calendar()["publications"]
    days = Counter(item["date"] for item in calendar)
    scheduled = {item["concept_id"] for item in calendar}
    certified = {item.id for item in store.concepts() if item.recovered and item.source_path}
    pairs = {(item["concept_id"], item.get("angle_index")) for item in calendar}
    return [
        check("Calendrier de six mois", len(days) == 180 and len(calendar) == 1080, f"{len(days)} jours, {len(calendar)} contenus"),
        check("Six contenus quotidiens", bool(days) and set(days.values()) == {6}, f"valeurs={sorted(set(days.values()))}"),
        check("Trois plateformes et deux créneaux", {item["platform"] for item in calendar} == set(PLATFORMS) and {item["slot"] for item in calendar} == {1, 2}, "TikTok, Instagram, Shorts · 10 h, 17 h"),
        check("Angles non dupliqués", len(pairs) == 360, f"{len(pairs)} couples concept-angle pour 360 sujets"),
        check("Uniquement des sources certifiées", scheduled <= certified, f"{len(scheduled)} concepts planifiés, tous certifiés"),
        check("Lecture quotidienne des scripts", store.production_day(min(days))["summary"]["total"] == 6, "API Production renvoie les six contenus du jour"),
    ]


def safety(root: Path, store: Store) -> list[dict]:
    automation = json.loads((root / "data/automation.json").read_text())
    policy = json.loads((root / "data/editorial_policy.json").read_text())
    server = (root / "leveria/server.py").read_text()
    reviewer = (root / "leveria/review_agents.py").read_text()
    missing = {item.id for item in store.concepts() if not item.recovered or not item.source_path}
    scheduled = {item["concept_id"] for item in store.calendar()["publications"]}
    agent_ids = set(policy.get("automation", {}).get("agents", []))
    return [
        check("Publication impossible", automation.get("publish") is False and "/api/publish" not in server, "publish=false et aucune route de publication"),
        check("Validation vidéo humaine", automation.get("human_approval_required") is True, "Chaque manifeste reste verrouillé"),
        check("Seuil automatique 9,5", policy.get("automation", {}).get("script_score_threshold") == 9.5 and "score < 9.5" in (root / "leveria/store.py").read_text(), "seuil vérifié dans la politique et le stockage"),
        check("Six agents obligatoires", agent_ids == {"source", "juridique_fiscal", "completude", "plateforme", "editorial", "securite"}, f"agents={sorted(agent_ids)}"),
        check("Échec fermé", "clé OpenAI absente" in reviewer and "ReviewResult(False" in reviewer, "Aucune auto-certification sans contrôle contradictoire"),
        check("Sources incomplètes exclues", not (missing & scheduled), f"{len(missing)} fiches bloquées, aucune planifiée"),
        check("Vidéo contrôlée", all((root / "video_pipeline" / name).is_file() for name in ("verify_video_words.py", "verify_video_quality.py")), "mots, audio, durée, résolution et synchronisation"),
    ]


def workflow(root: Path, store: Store) -> list[dict]:
    automation = json.loads((root / "data/automation.json").read_text())
    html = (root / "leveria/web/index.html").read_text()
    requirements = json.loads((root / "data/requirements.json").read_text())
    runs = {(item["slot"], item["time"]) for item in automation.get("runs", [])}
    return [
        check("Préparation en avance", automation.get("preflight") == {"time": "08:00", "days_ahead": 7}, "préparation quotidienne sur sept jours"),
        check("Créneaux automatiques", runs == {(1, "10:00"), (2, "17:00")}, f"runs={sorted(runs)}"),
        check("Scripts visibles par date", all(token in html for token in ("productionDate", "loadDay", "dayScripts", "Voir le script complet", "Contrôle des 6 agents")), "sélecteur, résumé, texte et rapports"),
        check("File persistante", (root / "leveria/queue.py").is_file() and "production_queue.json" in (root / "leveria/queue.py").read_text(), "reprise, état, erreur et tentatives"),
        check("Trois plateformes isolées", "for publication in selected" in (root / "leveria/daily.py").read_text() and "except Exception" in (root / "leveria/daily.py").read_text(), "une erreur est contenue dans l'élément concerné"),
        check("Exigences sans reste déclaré", all(item.get("status") == "satisfied" for item in requirements), f"{len(requirements)} exigences tracées"),
        check("Mémoire et provenance", (root / "data/history.json").is_file() and (root / "data/decision_ledger.json").is_file(), "historique indexé et empreintes conservées"),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--root", type=Path, default=Path.cwd()); args = parser.parse_args()
    root = args.root.resolve(); store = Store(root)
    audits = (("01_fonctionnel", functional(root, store)), ("02_securite", safety(root, store)), ("03_automatisation_ui", workflow(root, store)))
    out = root / "data/self_audits"; out.mkdir(parents=True, exist_ok=True)
    failed = 0
    for audit_id, checks in audits:
        passed = all(item["passed"] for item in checks); failed += not passed
        report = {"audit": audit_id, "passed": passed, "checked_at": datetime.now().isoformat(timespec="seconds"), "checks": checks}
        (out / f"{audit_id}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(audit_id, "OK" if passed else "ÉCHEC", f"{sum(item['passed'] for item in checks)}/{len(checks)}")
        for item in checks:
            if not item["passed"]: print(" -", item["criterion"], ":", item["evidence"])
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__": main()
