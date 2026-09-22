from dataclasses import dataclass


@dataclass(frozen=True)
class Family:
    id: str
    name: str
    description: str
    pillars: list[str]
    order: int


FAMILIES = [
    Family(
        id="assurance_vie",
        name="Assurance-vie",
        description="Enveloppe d'épargne, d'investissement et de transmission.",
        pillars=["epargner", "transmettre", "fiscalite"],
        order=1,
    ),
]