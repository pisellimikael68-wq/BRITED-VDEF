from abc import ABC, abstractmethod
from typing import Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseLLM(ABC):
    """
    Contrat commun à tous les fournisseurs de modèles de langage.
    """

    @abstractmethod
    def generate(
        self,
        *,
        prompt: str,
        response_model: Type[T],
        temperature: float = 0.2,
    ) -> T:
        """
        Génère une réponse structurée.
        """
        raise NotImplementedError
    