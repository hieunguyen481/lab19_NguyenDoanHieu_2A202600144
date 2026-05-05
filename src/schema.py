"""Shared schema definitions for the Day 19 GraphRAG pipeline."""

from __future__ import annotations

import re

ALLOWED_RELATIONS = {
    "FOUNDED_BY",
    "FOUNDED_IN",
    "HEADQUARTERED_IN",
    "HAS_CEO",
    "PARENT_OF",
    "DEVELOPS",
    "COMPETES_WITH",
    "PARTNERS_WITH",
    "INVESTS_IN",
    "OPERATES",
    "OPERATES_IN",
    "ACQUIRED",
    "ACQUIRED_IN",
    "ALIAS_OF",
}

SYMMETRIC_RELATIONS = {"COMPETES_WITH", "PARTNERS_WITH"}

NODE_TYPES = {"Company", "Person", "Product", "Location", "Year", "Sector", "Organization", "Entity"}

CANONICAL_ALIASES = {
    "google llc": "Google",
    "alphabet inc": "Alphabet",
    "openai inc": "OpenAI",
    "microsoft corp": "Microsoft",
    "microsoft azure": "Azure",
    "amazon web services": "AWS",
    "llama models": "Llama",
    "gpt models": "GPT models",
}

ENTITY_VARIANTS = {
    "Microsoft Azure": ["Microsoft Azure", "Azure"],
    "Amazon Web Services": ["Amazon Web Services", "AWS"],
    "Llama models": ["Llama models", "Llama"],
    "GPT models": ["GPT models", "GPT"],
}


def normalize_key(name: str) -> str:
    """Normalize entity names for alias lookup."""
    key = re.sub(r"[^a-zA-Z0-9\s]", "", name).strip().lower()
    return re.sub(r"\s+", " ", key)


def canonical_name(name: str) -> str:
    """Return the canonical graph node name for a raw entity string."""
    return CANONICAL_ALIASES.get(normalize_key(name), name.strip())
