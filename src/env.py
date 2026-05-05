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
    if os.getenv("USE_OPENAI_GENERATION", "0") != "1":
        return False
    key = os.getenv("OPENAI_API_KEY", "").strip()
    return bool(key and key != "your_openai_api_key_here")
