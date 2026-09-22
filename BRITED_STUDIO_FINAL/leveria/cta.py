from __future__ import annotations
from datetime import date

EDUCATIONAL = "pedagogique"
APPOINTMENT = "rendez_vous"
DISCUSSION = "discussion"
SAVE = "enregistrement"
FOLLOW = "abonnement"
# Most videos end with a useful takeaway, without an invitation.
ROTATION = (EDUCATIONAL, EDUCATIONAL, DISCUSSION, EDUCATIONAL,
            SAVE, EDUCATIONAL, EDUCATIONAL, FOLLOW,
            EDUCATIONAL, DISCUSSION, EDUCATIONAL, SAVE,
            EDUCATIONAL, APPOINTMENT)

def cta_mode(day: str | date, slot: int) -> str:
    day = date.fromisoformat(day) if isinstance(day, str) else day
    if slot not in (1, 2):
        raise ValueError("Le créneau CTA doit être 1 ou 2")
    return ROTATION[((day - date(2026, 9, 2)).days * 2 + slot - 1) % len(ROTATION)]

def cta_instruction(platform: str, mode: str) -> str:
    common = "Une seule invitation après une réponse complète. Ne demande aucun montant, document ou détail personnel en commentaire. "
    if mode == APPOINTMENT:
        return common + "Propose sobrement un contact via le profil, sans urgence ni promesse. N'impose pas la formulation historique de rendez-vous."
    if mode == SAVE:
        return common + "Invite à enregistrer la vidéo pour retrouver le repère concret expliqué. Relie cette invitation au sujet."
    if mode == FOLLOW:
        return common + "Invite à s'abonner pour suivre la série patrimoniale concernée, en précisant ce que le spectateur pourra y comprendre."
    if mode == EDUCATIONAL:
        return "Termine par une idée utile à retenir ou un réflexe concret. Aucune invitation à commenter, enregistrer, s’abonner ou prendre rendez-vous."
    if mode == DISCUSSION:
        return common + "Pose une question précise de compréhension ou de prochain thème, avec une invitation à répondre en commentaire. Ne simule pas une question déjà reçue."
    raise ValueError("Mode CTA inconnu : " + str(mode))
