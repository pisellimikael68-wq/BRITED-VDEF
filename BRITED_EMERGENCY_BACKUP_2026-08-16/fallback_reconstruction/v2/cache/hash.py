import hashlib


def compute_hash(text: str) -> str:
    """
    Calcule le hash SHA256 d'un texte.
    """

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()
