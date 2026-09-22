import re
import unicodedata


def slugify(text: str) -> str:
    """
    Transforme un titre en identifiant de fichier.

    Exemple :
        "Clause bénéficiaire" -> "clause_beneficiaire"
    """

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    text = text.lower()

    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)

    return text.strip("_")
