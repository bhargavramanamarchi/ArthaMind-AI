"""
ArthaMind AI — Configuration Module
====================================
Centralized configuration management for the entire application.
Loads environment variables, validates API keys, and provides
typed settings for all modules.
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# ── Load .env ────────────────────────────────────────────────
load_dotenv()

# ── Project Paths ────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
LOGS_DIR = BASE_DIR / "logs"
CHROMA_DIR = DATA_DIR / "chroma_db"

# Ensure directories exist
for _dir in [DATA_DIR, ASSETS_DIR, LOGS_DIR, CHROMA_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)


class Settings:
    """Centralized application settings loaded from environment variables."""

    # ── API Keys ─────────────────────────────────────────────
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    ASSEMBLYAI_API_KEY: str = os.getenv("ASSEMBLYAI_API_KEY", "")
    MURF_API_KEY: str = os.getenv("MURF_API_KEY", "")
    GOLDAPI_KEY: str = os.getenv("GOLDAPI_KEY", "")

    # ── LLM Configuration ───────────────────────────────────
    LLM_MODEL: str = "gemini-2.5-flash"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 4096

    # ── Embedding Configuration ─────────────────────────────
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DEVICE: str = "cpu"

    # ── RAG Configuration ───────────────────────────────────
    CHROMA_COLLECTION: str = "arthamind_knowledge"
    RAG_CHUNK_SIZE: int = 1000
    RAG_CHUNK_OVERLAP: int = 200
    RAG_TOP_K: int = 5

    # ── Voice Configuration ─────────────────────────────────
    TTS_FALLBACK: str = "gtts"  # "murf" or "gtts"

    # ── App Configuration ───────────────────────────────────
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    GRADIO_SERVER_PORT: int = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    GRADIO_SHARE: bool = os.getenv("GRADIO_SHARE", "false").lower() == "true"
    APP_TITLE: str = "ArthaMind AI"
    APP_TAGLINE: str = "Your Intelligent Personal Finance Advisor for Indian Citizens"

    # ── Supported Languages ─────────────────────────────────
    SUPPORTED_LANGUAGES: dict[str, str] = {
        "English": "en",
        "हिन्दी (Hindi)": "hi",
        "తెలుగు (Telugu)": "te",
        "தமிழ் (Tamil)": "ta",
        "ಕನ್ನಡ (Kannada)": "kn",
        "മലയാളം (Malayalam)": "ml",
    }

    # ── Language Codes for TTS ──────────────────────────────
    GTTS_LANGUAGE_MAP: dict[str, str] = {
        "en": "en",
        "hi": "hi",
        "te": "te",
        "ta": "ta",
        "kn": "kn",
        "ml": "ml",
    }

    # ── GST Slabs ───────────────────────────────────────────
    GST_SLABS: list[float] = [0.0, 5.0, 12.0, 18.0, 28.0]

    # ── Currency List ───────────────────────────────────────
    CURRENCIES: list[str] = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "SGD", "AED", "SAR", "CHF"]

    @classmethod
    def validate(cls) -> dict[str, bool]:
        """Validate which API keys are configured.

        Returns:
            Dictionary mapping service names to availability status.
        """
        return {
            "gemini": bool(cls.GOOGLE_API_KEY and cls.GOOGLE_API_KEY != "your_google_api_key_here"),
            "assemblyai": bool(cls.ASSEMBLYAI_API_KEY and cls.ASSEMBLYAI_API_KEY != "your_assemblyai_api_key_here"),
            "murf": bool(cls.MURF_API_KEY and cls.MURF_API_KEY != "your_murf_api_key_here"),
            "goldapi": bool(cls.GOLDAPI_KEY and cls.GOLDAPI_KEY != "your_goldapi_key_here"),
        }

    @classmethod
    def get_available_services(cls) -> str:
        """Return a human-readable summary of available services."""
        status = cls.validate()
        lines = []
        for service, available in status.items():
            icon = "✅" if available else "❌"
            lines.append(f"{icon} {service.upper()}")
        return "\n".join(lines)


# ── Singleton instance ──────────────────────────────────────
settings = Settings()
