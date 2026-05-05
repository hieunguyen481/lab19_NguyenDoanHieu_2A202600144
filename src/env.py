"""Environment loading helpers."""

from __future__ import annotations

import os

from .paths import ROOT_DIR


def load_environment() -> None:
    """Load .env from Day19 root when python-dotenv is available."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(ROOT_DIR / ".env")


def openai_enabled() -> bool:
    """Return True when an OpenAI API key is configured."""
    return bool(os.getenv("OPENAI_API_KEY"))
