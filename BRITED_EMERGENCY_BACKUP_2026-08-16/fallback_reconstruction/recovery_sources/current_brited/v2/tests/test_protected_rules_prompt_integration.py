from pathlib import Path

from v2.agents.models import PlannedTopic
from v2.services.llm_service import LLMService


def main() -> None:

    print("=" * 70)
    print("PROTECTED RULES PROMPT INTEGRATION TEST")
    print("=" * 70)

    topic = PlannedTopic(
        id=(
            "assurance_vie_fiscalite_"
            "rachat_legal_tax_test"
        ),
        title=(
            "Fiscalité du rachat en assurance-vie"
        ),
        editorial_order=1,
    )

    service = LLMService()

    prompt = service.build_topic_prompt(
        family="assurance_vie",
        chapter="fiscalite",
        topic=topic,
    )

    prompt_hash = service.compute_topic_prompt_hash(
        family="assurance_vie",
        chapter="fiscalite",
        topic=topic,
    )

    checks = {
        "Bloc règles protégées": (
            "RÈGLES TECHNIQUES PROTÉGÉES"
            in prompt
        ),
        "Formule rachat partiel": (
            "montant du rachat / valeur de rachat"
            in prompt
        ),
        "27 septembre 2017": (
            "27 septembre 2017"
            in prompt
        ),
        "150 000": (
            "150 000"
            in prompt
        ),
        "Taux 7,5 %": (
            "7,5 %"
            in prompt
        ),
        "Taux 12,8 %": (
            "12,8 %"
            in prompt
        ),
        "Interdiction exonération": (
            (
                "ne constitue pas une exonération générale"
                in prompt
            )
        ),
        "Interdiction inversion formule": (
            "inverser une formule"
            in prompt
        ),
        "Interdiction modifier assiette": (
            "modifier l'assiette d'un calcul"
            in prompt
        ),
    }

    print()

    for label, result in checks.items():

        print(
            f"{label:<35} : {result}"
        )

    print()
    print("=" * 70)
    print("HASH")
    print("=" * 70)

    print(prompt_hash)

    print()
    print("=" * 70)
    print("HASH INVALIDATION")
    print("=" * 70)

    knowledge_file = Path(
        "data/knowledge/academic/"
        "assurance_vie/rachats.json"
    )

    original_content = knowledge_file.read_text(
        encoding="utf-8"
    )

    try:

        modified_content = original_content.replace(
            (
                "Un montant de primes inférieur au seuil "
                "de 150 000 euros ne constitue pas une "
                "exonération générale d'impôt sur le revenu."
            ),
            (
                "Un montant de primes inférieur au seuil "
                "de 150 000 euros ne constitue jamais, "
                "à lui seul, une exonération générale "
                "d'impôt sur le revenu."
            ),
        )

        if modified_content == original_content:

            raise AssertionError(
                "La règle protégée cible n'a pas été trouvée "
                "dans le fichier Knowledge."
            )

        knowledge_file.write_text(
            modified_content,
            encoding="utf-8",
        )

        service_after = LLMService()

        hash_after = (
            service_after.compute_topic_prompt_hash(
                family="assurance_vie",
                chapter="fiscalite",
                topic=topic,
            )
        )

        print(
            "HASH AVANT  :",
            prompt_hash,
        )

        print(
            "HASH APRÈS  :",
            hash_after,
        )

        print(
            "HASH MODIFIÉ :",
            prompt_hash != hash_after,
        )

    finally:

        knowledge_file.write_text(
            original_content,
            encoding="utf-8",
        )

        print(
            "CORPUS RESTAURÉ : True"
        )

    print()
    print("=" * 70)
    print("RÉSULTAT GLOBAL")
    print("=" * 70)

    all_valid = all(checks.values())

    print(
        "PROMPT VALIDE :",
        all_valid,
    )

    if not all_valid:

        failed_checks = [
            label
            for label, result in checks.items()
            if not result
        ]

        raise AssertionError(
            "Contrôles échoués : "
            + ", ".join(failed_checks)
        )


if __name__ == "__main__":

    main()
    