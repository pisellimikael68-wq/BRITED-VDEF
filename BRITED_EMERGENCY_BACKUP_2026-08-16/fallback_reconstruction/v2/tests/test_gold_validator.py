from v2.knowledge.registry import KnowledgeRegistry
from v2.knowledge.validators.gold_validator import GoldValidator


def main():

    registry = KnowledgeRegistry()

    topic = registry.get_topic(
        "assurance_vie_fondamentaux_definition"
    )

    report = GoldValidator().validate(topic)

    print("=" * 60)
    print("GOLD VALIDATOR")
    print("=" * 60)

    print(f"Passed      : {report.passed_rules}")
    print(f"Failed      : {report.failed_rules}")
    print(f"Warnings    : {report.warnings}")
    print(f"Suggestions : {report.suggestions}")


if __name__ == "__main__":
    main()
    