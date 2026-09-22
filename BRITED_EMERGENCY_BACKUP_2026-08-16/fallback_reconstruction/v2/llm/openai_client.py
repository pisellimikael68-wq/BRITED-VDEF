import json
import os
from typing import Type, TypeVar

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError

from v2.core.logger import get_logger

from .base import BaseLLM

load_dotenv()

T = TypeVar("T", bound=BaseModel)


class OpenAILLM(BaseLLM):
    """
    Implémentation OpenAI du moteur LLM.
    """

    def __init__(self):

        self.logger = get_logger(__name__)

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY introuvable dans le fichier .env."
            )

        self.client = OpenAI(
            api_key=api_key,
            timeout=60.0,
        )

    def generate(
        self,
        *,
        prompt: str,
        response_model: Type[T],
        temperature: float = 0.2,
    ) -> T:

        self.logger.info("🤖 Appel GPT")

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )

        self.logger.info("✅ Réponse GPT reçue")

        content = response.output_text.strip()

        # Gestion d'un éventuel bloc ```json
        if content.startswith("```"):
            content = (
                content.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        self.logger.info("📦 Parsing JSON")

        try:
            data = json.loads(content)

        except json.JSONDecodeError as e:

            self.logger.error("❌ JSON invalide")

            raise ValueError(
                f"Le modèle n'a pas renvoyé un JSON valide :\n\n{content}"
            ) from e

        self.logger.info("✅ Validation du schéma")

        try:

            result = response_model.model_validate(data)

        except ValidationError as e:

            self.logger.error("❌ Validation Pydantic échouée")

            raise ValueError(
                f"Le JSON ne correspond pas au schéma "
                f"{response_model.__name__}"
            ) from e

        self.logger.info("✅ Topic validé")

        return result
    