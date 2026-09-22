from dataclasses import dataclass, field

from v2.models.knowledge_models import Topic


@dataclass
class PlanningWeek:
    week: int
    topics: list[Topic] = field(default_factory=list)


@dataclass
class Planning:
    family: str
    weeks: list[PlanningWeek] = field(default_factory=list)

    def display(self):

        print("\n")
        print("=" * 60)
        print(f"📅 PLANNING ÉDITORIAL - {self.family.upper()}")
        print("=" * 60)

        days = [
            "Lundi",
            "Mercredi",
            "Vendredi",
            "Dimanche",
        ]

        for week in self.weeks:

            print(f"\n📆 Semaine {week.week}")
            print("-" * 40)

            for day, topic in zip(days, week.topics):
                print(f"{day:<12} {topic.title}")