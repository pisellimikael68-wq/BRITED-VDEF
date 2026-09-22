from enum import Enum


class ValidationSeverity(Enum):
    """
    Niveau de gravité d'une anomalie détectée
    lors de la validation du corpus.
    """

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    