from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from .audit import audit_script
from .store import Store, PLATFORM_LABELS


PROMPT = """Tu écris pour BRITED Studio, média pédagogique français de gestion de patrimoine.
Rédige un script natif {platform} sur le concept « {title} » ({concept_id}).
Contraintes absolues : exactitude juridique/fiscale, règle bornée, exception utile, exemple concret,
question adressée au spectateur, réponse après la question, conclusion courte et sources officielles.
Ne fabrique aucun chiffre ni article. Si l'information source est insuffisante, écris exactement
SOURCE INSUFFISANTE. Format Markdown : titre, tableau Beat/Narration/Visuel/Texte écran,
Narration continue, Sources. Durée visée : 38 à 52 secondes, jamais plus de 60 secondes.
"""


def generate(store: Store, publication_id: str) -> dict:
    publication = store.publication(publication_id)
    concept = next(c for c in store.concepts() if c.id == publication["concept_id"])
    source = ""
    if concept.source_path:
        source = (store.root / concept.source_path).read_text(encoding="utf-8", errors="ignore")
    if not source.strip():
        raise RuntimeError("Source conceptuelle absente : génération bloquée pour éviter une erreur factuelle")
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Clé OpenAI absente. Ajoutez-la uniquement dans le fichier .env local.")
    request_body = {
        "model": os.environ.get("BRITED_MODEL", "gpt-5-mini"),
        "input": PROMPT.format(platform=PLATFORM_LABELS.get(publication["platform"], publication["platform"]),
                               title=concept.titre, concept_id=concept.id) + "\n\nSOURCE VALIDÉE :\n" + source,
    }
    request = urllib.request.Request("https://api.openai.com/v1/responses",
        data=json.dumps(request_body).encode(), headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"API OpenAI : erreur {error.code}") from None
    text = data.get("output_text") or "".join(
        block.get("text", "") for item in data.get("output", []) for block in item.get("content", [])
        if block.get("type") == "output_text"
    )
    if not text or "SOURCE INSUFFISANTE" in text:
        raise RuntimeError("La génération a été bloquée faute de source suffisante")
    folder = store.scripts / concept.domaine
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / f"{concept.id}__{publication['platform']}__a{publication.get('angle_index', 0)+1}.md"
    target.write_text(text.strip() + "\n", encoding="utf-8")
    audit = audit_script(text, publication["platform"])
    status = "script_valide" if audit.ok else "a_corriger"
    store.update_publication(publication_id, script_path=str(target.relative_to(store.root)), statut=status)
    return {"path": str(target.relative_to(store.root)), "audit": audit.json(), "status": status}
