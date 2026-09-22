from __future__ import annotations

import json
import os
import re
import ssl
import urllib.error
import urllib.request
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from .audit import audit_script
from .performance import score_script
from .format_adapter import adapt_beats, beats_from_markdown
from .usage import record_api_usage
from .local_llm import LocalAIUnavailable, call_local

try:
    import certifi
    TLS_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    TLS_CONTEXT = ssl.create_default_context()


AGENTS = {
    "source": "Fidélité stricte aux faits, chiffres, dates, conditions et sources de la fiche BRITED.",
    "juridique_fiscal": "Exactitude juridique et fiscale, limites, exceptions et absence de généralisation trompeuse.",
    "completude": "Réponse complète malgré la concision, exemple utile, nuance indispensable et absence d'omission dangereuse.",
    "plateforme": "Respect du format natif, de l'ordre des séquences, de la durée et des usages de la plateforme.",
    "editorial": "Accroche, clarté, fluidité, interaction, ton direct, mémorisation et apprentissage d'une règle utile avant l'appel à l'action.",
    "securite": "Contenu pédagogique, neutre, sourcé, sans conseil personnalisé ni affirmation non étayée.",
    "formulation_professionnelle": "Contrôle phrase par phrase d'un français naturel, immédiatement compréhensible, précis, crédible et adapté à une conversation pédagogique avec un ami.",
    "contre_verification_finale": "Seconde lecture indépendante de l'ensemble du script : sens des phrases, enchaînements, prononciation, libellés internes, cohérence question-réponse et appel à l'action.",
    "coherence_pictogrammes": "Contrôle page par page que le visuel décrit illustre précisément la notion prononcée, sans symbole générique, ambigu, décoratif ou sans rapport.",
    "densite_editoriale": "Vérifie que la vidéo traite un seul angle et reste concise sans perdre la règle centrale, sa condition, l'exception indispensable, l'exemple utile, les chiffres ni les sources.",
    "pedagogie_client": "Se place comme une personne sans aucune culture patrimoniale : situation familière, vocabulaire courant, terme technique immédiatement traduit, règle mémorisable, exemple parlant qui projette explicitement le spectateur dans la situation et réflexe pratique immédiatement utilisable ; pour la Finance, la nature exacte du produit doit être nommée.",
    "retention_attention": "Contrôle la force des deux premières secondes, la progression de curiosité, l'absence de longueur et l'utilité de chaque phrase jusqu'au CTA.",
    "impact_dynamique": "Bloque tout script qui ressemble à un cours : exige un hook spécifique qui arrête le défilement, une valeur concrète dès la phrase suivante, des phrases nerveuses, un réflexe pratique avant le CTA et une progression orale rapide sans sensationnalisme.",
    "conversion_confiance": "Vérifie que la vidéo apporte toute sa valeur avant le CTA et construit un vivier de prospects par la confiance, sans rétention d'information, peur artificielle, surpromesse ni pression commerciale.",
    "fluidite_orale": "Lit le texte à voix haute mentalement et bloque toute formulation télégraphique, ponctuation cassante, répétition, liaison difficile ou enchaînement susceptible de produire une diction artificielle. Chaque phrase doit répondre à la précédente ou en reprendre naturellement l'idée, puis préparer la suivante, sans effet de liste.",
}

AGENT_RESULT_SCHEMA = {
    "type": "object",
    "properties": {
        "agents": {
            "type": "object",
            "properties": {
                agent_id: {
                    "type": "object",
                    "properties": {
                        "score": {"type": "number"},
                        "passed": {"type": "boolean"},
                        "findings": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["score", "passed", "findings"],
                }
                for agent_id in AGENTS
            },
            "required": list(AGENTS),
        },
        "recommendations": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["agents", "recommendations"],
}


@dataclass(frozen=True)
class ReviewResult:
    passed: bool
    threshold: float
    overall: float
    agents: dict[str, dict[str, Any]]
    deterministic: dict[str, Any]
    errors: tuple[str, ...]
    recommendations: tuple[str, ...]
    reviewed_at: str
    model: str

    def json(self) -> dict[str, Any]:
        return asdict(self)


def _output_text(data: dict[str, Any]) -> str:
    if data.get("output_text"):
        return str(data["output_text"])
    return "".join(
        str(block.get("text", ""))
        for item in data.get("output", [])
        for block in item.get("content", [])
        if block.get("type") == "output_text"
    )


def _json_from_text(text: str) -> dict[str, Any]:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I | re.S)
    return json.loads(cleaned)


def review_script(source: str, script: str, platform: str, *, threshold: float = 10.0, root: Path | None = None) -> ReviewResult:
    audit = audit_script(script, platform)
    performance = score_script(script, platform)
    parsed_beats = beats_from_markdown(script)
    adaptation = None
    if parsed_beats:
        try:
            _, format_report = adapt_beats(parsed_beats, platform)
            adaptation = format_report.json()
        except ValueError as error:
            adaptation = {"passed": False, "error": str(error)}
    deterministic = {"audit": audit.json(), "performance": performance, "format_adaptation": adaptation}
    errors = list(audit.errors)
    recommendations = list(audit.warnings)
    if not parsed_beats:
        errors.append("Agent de format : aucun beat exploitable dans le tableau")
    elif not adaptation or not adaptation.get("passed"):
        errors.append("Agent de format : adaptation exacte impossible")
    root = (root or Path(os.environ.get("BRITED_ROOT", Path(__file__).resolve().parents[1]))).resolve()
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    external_review = os.environ.get("BRITED_EXTERNAL_REVIEW", "0").strip() == "1"
    automation_path = root / "data" / "automation.json"
    automation = json.loads(automation_path.read_text(encoding="utf-8")) if automation_path.exists() else {}
    external_config = automation.get("external_ai", {})
    prefer_external = bool(external_config.get("prefer_for_strict_certification", False))
    external_review = external_review or (
        bool(external_config.get("enabled", False))
        and bool(external_config.get("manual_approval_granted", False))
    )
    model = os.environ.get("BRITED_REVIEW_MODEL", os.environ.get("BRITED_MODEL", "gpt-5-mini"))
    prompt = f"""Tu es le comité de certification BRITED. Compare le script à la source de vérité.
Plateforme : {platform}
Seuil obligatoire : {threshold}/10 POUR CHAQUE AGENT. Une moyenne ne compense jamais une faiblesse.

SOURCE CERTIFIÉE :
{source}

SCRIPT À CONTRÔLER :
{script}

Évalue ces agents :
{json.dumps(AGENTS, ensure_ascii=False, indent=2)}

Règles absolues :
- Format validé le 11 septembre 2026 : vidéo de 60 à 65 secondes, cible 63 secondes. Préparer environ 150 à 165 mots prononcés, nombres développés, à un débit naturel autour de 160 mots/minute avec des pauses. Ce budget est indicatif : chronométrer la lecture puis le montage final, jingle compris. Si un jingle est ajouté, déduire sa durée du budget de parole ; ne pas accélérer artificiellement. Un texte seul ne garantit pas la durée réelle ni une rémunération TikTok.
- Parle comme à un ami en le vouvoyant : vous, votre, vos. Une situation familière, une seule idée, un exemple concret avec les chiffres utiles, une explication de ce que cela change pour lui et une conclusion utile. Pas de dialogue fictif à deux voix, pas de témoignage inventé, pas de tic systématique comme imaginez ou vous voyez.
- Refuser les répétitions ajoutées uniquement pour atteindre une minute ; resserrer le sous-angle si les conditions ne tiennent pas dans le format.
- Distinguer validation du texte et durée mesurée : ne jamais certifier la durée finale à partir du seul nombre de mots ;
- 10/10 signifie publiable sans aucune modification identifiable ; 9,9/10 ou moins est refusé ;
- aucune moyenne ne compense une faiblesse : chaque agent doit rendre exactement 10, passed true et findings [] ;
- ne recopie jamais la description d'un agent dans findings : ce n'est pas une anomalie ;
- si aucune erreur précise et localisable n'existe pour un agent, attribue 10, passed true et findings [] ;
- une note inférieure à {threshold} exige au moins un finding concret citant la phrase, le fait ou l'élément exact en cause ; toute réserve générique est interdite ;
- n'utilise pas mécaniquement la note 9 : le seuil est bloquant et doit refléter une erreur réelle, pas une prudence abstraite ;
- aucune information absente de la source ne peut être acceptée ;
- toute condition, exception ou limite déterminante doit être conservée ;
- juge la complétude par rapport à l'angle précis annoncé par le titre et le hook, pas par rapport à tous les sujets connexes présents dans la fiche source ;
- n'exige jamais l'ajout d'une formalité, d'un cas particulier ou d'un autre mécanisme qui ne conditionne pas la véracité de l'angle central ; ces éléments doivent faire l'objet d'un contenu distinct ;
- pour un contenu sur les effets du régime matrimonial applicable sans contrat, n'exige pas la procédure permettant de changer ultérieurement de régime, sauf si le script prétend que ce régime est irrévocable ou impossible à modifier ;
- pour un format court, considère le propos complet s'il contient la règle centrale, sa condition d'application, l'exception indispensable pour ne pas induire en erreur et un exemple parlant ;
- ne pénalise pas le script parce qu'une information est réservée au texte écran ou aux sources, si sa lecture à voix haute rendrait le format artificiellement dense ;
- vérifie les chiffres, articles, exemples et formulations un par un ;
- lis chaque phrase entière, isolément puis dans son enchaînement : une tournure télégraphique, maladroite, ambiguë ou dont le référent n'est pas évident est bloquante ;
- le hook et la question doivent pouvoir être compris immédiatement par une personne non spécialiste, tout en conservant un ton sérieux et professionnel ; ils nomment l'action, son objet et l'enjeu sans dépendre du titre, de la miniature ou d'une connaissance métier ;
- refuse les libellés de fabrication ou les amorces artificielles dans la narration (par exemple « Court : », « Règle : », « Question : » ou « Réponse : ») ;
- vérifie que la réponse répond exactement à la question, avec le même périmètre et sans changement silencieux de sujet ;
- tout nombre doit pouvoir être prononcé comme un nombre français complet et naturel, jamais chiffre par chiffre ;
- l'agent coherence_pictogrammes compare, pour chaque beat, la narration et la colonne Visuel ; chaque symbole doit rendre la notion immédiatement compréhensible et un pictogramme générique est bloquant ;
- l'agent densite_editoriale refuse à la fois les répétitions évitables et toute concision obtenue en supprimant une information indispensable ; si plusieurs règles principales sont mélangées, il impose un sous-angle autonome ou une mini-série ;
- l'agent contre_verification_finale doit effectuer une seconde lecture indépendante de toutes les phrases et ne peut pas se contenter des notes des autres agents ;
- une conclusion pédagogique peut se terminer sans appel à agir ; ne jamais imposer un commentaire, un abonnement ou un rendez-vous pour obtenir la validation ;
- une question simple et précise suffit comme accroche ; ne pas ajouter de peur, de jargon ou de suspense pour la rendre spectaculaire ;
- l'agent pedagogie_client doit simuler une première écoute par un non-spécialiste et refuser toute phrase nécessitant de deviner le référent ou le mécanisme ;
- si le titre ou la question contient « quand », « à quel âge » ou « à quel moment », l'agent pedagogie_client refuse le script tant qu'il ne fournit pas un repère de décision concret avec ses conditions ; une simple explication du mécanisme ne répond pas à la promesse ;
- l'agent pedagogie_client refuse toute formule, règle de calcul ou notion secondaire qui ajoute de la charge mentale sans modifier l'action à retenir ; un mécanisme abstrait doit être expliqué avec des mots compréhensibles par un enfant et une comparaison simple ;
- l'agent pedagogie_client exige un mini-apprentissage autonome : une situation reconnaissable, une règle formulée en mots courants, un exemple concret et un point que le spectateur peut vérifier dans sa propre situation ;
- l'agent pedagogie_client exige avant le CTA un réflexe précis et immédiatement utilisable : document à lire, chiffre à comparer, date à conserver, clause à vérifier, simulation à faire ou question concrète à poser ; une injonction générique comme « renseignez-vous » ne vaut pas 10/10 ;
- l'agent pedagogie_client exige que l'exemple inclue explicitement le spectateur avec une projection naturelle contenant « vous », « votre » ou « vos », par exemple « Imaginez que vous… », « Prenons votre cas » ou « Si vous… » ; il refuse un exemple froid décrit à la troisième personne et refuse aussi la répétition mécanique de la même amorce dans tous les scripts ;
- tout terme technique indispensable doit être expliqué immédiatement dans la narration ; une définition juridique exacte mais incompréhensible au grand public est bloquante ;
- pour tout sujet Finance portant sur un produit déterminé, le titre ou l'accroche doit nommer explicitement sa nature exacte ; si la fiche source traite seulement d'un mécanisme financier général, accepte sa désignation précise sans exiger ni inventer un produit absent de la source ; refuse toujours « votre contrat » ou « ce contrat » lorsque son type n'est pas présent dans la même phrase ;
- l'agent retention_attention doit refuser toute amorce générique, répétition, suspense artificiel, transition sans utilité ou phrase qui n'apporte ni compréhension ni progression ;
- l'agent impact_dynamique doit se placer dans la situation d'une personne qui fait défiler son fil : il refuse le script si les deux premières secondes ne créent aucune tension concrète, si la valeur tarde, si le texte annonce un sujet comme un cours, si l'énergie reste uniforme ou si une phrase peut être supprimée sans perte ;
- pour impact_dynamique, un hook 10/10 est court, spécifique au sujet et centré sur une conséquence vécue par le spectateur ; une simple question générique ou « saviez-vous que » ne suffit pas ;
- l'agent conversion_confiance doit refuser tout ton robotique, sensationnaliste ou approximatif susceptible de diminuer la crédibilité professionnelle ;
- l'agent conversion_confiance doit aussi refuser une information volontairement incomplète destinée à forcer le rendez-vous : l'utilité doit être entière avant le CTA, qui suit le calendrier : idée utile sans invitation, discussion, enregistrement, abonnement ou contact discret ; aucun rendez-vous systématique ;
- l'agent fluidite_orale doit contrôler chaque liaison entre phrases et entre pages, ainsi que les groupes de souffle, la ponctuation et les successions de consonnes ; toute diction prévisiblement heurtée ou artificielle est bloquante ;
- un doute factuel, juridique ou fiscal impose une note inférieure au seuil ;
- findings contient uniquement les erreurs ou réserves bloquantes, jamais les qualités constatées ;
- si une amélioration précise est encore possible, la note ne peut pas être 10 et cette amélioration doit devenir un finding bloquant ; recommendations doit être vide pour toute version certifiée ;
- réponds uniquement selon le schéma JSON imposé ; attribue les notes réellement constatées et ne recopie jamais des valeurs d'exemple ou des valeurs par défaut.
"""
    payload = None
    local_error: Exception | None = None
    if not prefer_external:
        try:
            local_text, local_model = call_local(root, prompt, json_output=AGENT_RESULT_SCHEMA)
            if os.environ.get("BRITED_DEBUG_REVIEW") == "1":
                debug = root / "data" / "reviews" / "_last_local_raw.json"
                debug.parent.mkdir(parents=True, exist_ok=True)
                debug.write_text(local_text, encoding="utf-8")
            payload = _json_from_text(local_text)
            model = f"ollama:{local_model}"
        except (LocalAIUnavailable, json.JSONDecodeError, KeyError, ValueError) as exc:
            local_error = exc
    if payload is None:
        if not external_review:
            errors.append(f"Contrôle contradictoire local indisponible en mode zéro token : {local_error}. Aucun token externe consommé")
            return ReviewResult(False, threshold, 0.0, {}, deterministic, tuple(errors), tuple(recommendations), datetime.now().isoformat(timespec="seconds"), "local-only")
        if not key:
            errors.append("Contrôle contradictoire externe autorisé mais clé OpenAI absente")
            return ReviewResult(False, threshold, 0.0, {}, deterministic, tuple(errors), tuple(recommendations), datetime.now().isoformat(timespec="seconds"), model)

    body = {"model": model, "input": prompt, "reasoning": {"effort": "low"}, "max_output_tokens": 3000}
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    last_error: Exception | None = None
    if payload is None:
        for attempt in range(3):
            try:
                with urllib.request.urlopen(request, timeout=300, context=TLS_CONTEXT) as response:
                    response_data = json.load(response)
                    record_api_usage(response_data, "certification", model)
                    payload = _json_from_text(_output_text(response_data))
                break
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, json.JSONDecodeError, KeyError) as exc:
                last_error = exc
                if isinstance(exc, urllib.error.HTTPError) and 400 <= exc.code < 500 and exc.code != 429:
                    break
                if attempt < 2: time.sleep((attempt + 1) * 2)
    if payload is None:
        errors.append(f"Contrôle contradictoire indisponible après reprise : {type(last_error).__name__}")
        return ReviewResult(False, threshold, 0.0, {}, deterministic, tuple(errors), tuple(recommendations), datetime.now().isoformat(timespec="seconds"), model)

    agents: dict[str, dict[str, Any]] = {}
    # Certains modèles locaux respectent les champs mais omettent l'enveloppe
    # `agents`. Accepter les deux formes évite de transformer un rapport réel
    # en huit faux zéros, sans jamais relâcher le seuil de certification.
    payload_agents = payload.get("agents") if isinstance(payload.get("agents"), dict) else payload
    for agent_id in AGENTS:
        raw = payload_agents.get(agent_id, {}) if isinstance(payload_agents, dict) else {}
        score = max(0.0, min(10.0, float(raw.get("score", 0))))
        findings = [str(item) for item in raw.get("findings", [])]
        passed = bool(raw.get("passed", False)) and score == 10.0 and not findings
        agents[agent_id] = {"label": AGENTS[agent_id], "score": score, "passed": passed, "findings": findings}
        if not passed:
            errors.extend(f"{agent_id} : {item}" for item in findings or [f"note {score:g}/10"])
    recommendations.extend(str(item) for item in payload.get("recommendations", []))
    scores = [item["score"] for item in agents.values()]
    overall = round(sum(scores) / len(scores), 2) if scores else 0.0
    passed = bool(
        audit.ok
        and not audit.warnings
        and performance.get("overall", 0) == 10.0
        and agents
        and all(item["passed"] and item["score"] == 10.0 for item in agents.values())
        and not recommendations
    )
    if performance.get("overall", 0) < threshold:
        errors.append(f"Performance plateforme : {performance.get('overall', 0)}/10, seuil {threshold}/10")
    return ReviewResult(passed, threshold, overall, agents, deterministic, tuple(dict.fromkeys(errors)), tuple(dict.fromkeys(recommendations)), datetime.now().isoformat(timespec="seconds"), model)


def save_review(root: Path, publication_id: str, script_path: str, result: ReviewResult) -> str:
    folder = root / "data" / "reviews"
    folder.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^a-zA-Z0-9_-]+", "_", publication_id)
    target = folder / f"{safe}.json"
    payload = result.json(); payload["publication_id"] = publication_id; payload["script_path"] = script_path
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return str(target.relative_to(root))
