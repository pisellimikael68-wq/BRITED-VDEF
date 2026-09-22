"""Compatibilité avec les anciens outils BRITED, sans secret dans le code."""
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

LEVERIA_PATH = "/Users/mikael_piselli/Documents/GitHub/leveria-knowledge"

VECTOR_STORE_ID = "vs_6a4263ee654c81919764c1a7fc7dc9fe"
MIN_REVIEW_SCORE = 90
