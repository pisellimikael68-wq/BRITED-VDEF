import json

from pathlib import Path
from datetime import datetime


class HistoryManager:

    def save(self, context):

        history_dir = Path("history")
        history_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        history_file = history_dir / "history.json"

        if history_file.exists():

            with open(
                history_file,
                "r",
                encoding="utf-8",
            ) as f:

                try:
                    history = json.load(f)

                except Exception:
                    history = []

        else:

            history = []

        review = context.review
        angle = context.selected_angle
        script = context.script

        history.append({

            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "pipeline": "instagram",

            "version": "1.0",

            "subject": context.subject,

            "title": script.title,

            "angle": angle.title if angle else "",

            "score": review.score if review else 0,

        })

        with open(
            history_file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                history,
                f,
                indent=4,
                ensure_ascii=False,
            )

        return history_file
    