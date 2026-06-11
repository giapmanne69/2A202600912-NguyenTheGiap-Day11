"""
Lab 11 — Configuration & API Key Setup
"""
import os
from pathlib import Path


DEFAULT_GEMINI_MODEL = "gemini-2.5-flash-lite"
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def _load_env_file():
    """Load .env (repo root preferred) if python-dotenv is available."""
    try:
        from dotenv import load_dotenv
    except Exception:
        return

    repo_root = Path(__file__).resolve().parents[2]
    root_env = repo_root / ".env"
    src_env = Path(__file__).resolve().parents[1] / ".env"

    if root_env.exists():
        load_dotenv(dotenv_path=root_env, override=False)
    elif src_env.exists():
        load_dotenv(dotenv_path=src_env, override=False)


def get_model_name() -> str:
    """Return active model string for ADK calls.

    Priority:
    1) OPENAI_MODEL from .env/environment (OpenRouter/OpenAI style)
    2) default Gemini model
    """
    raw_model = os.getenv("OPENAI_MODEL", "").strip()
    if raw_model:
        # Use user-provided model string exactly as configured in .env.
        return raw_model
    return DEFAULT_GEMINI_MODEL


def using_openai_backend() -> bool:
    """Check whether OpenAI/OpenRouter backend should be used."""
    return bool(os.getenv("OPENAI_API_KEY", "").strip() and os.getenv("OPENAI_MODEL", "").strip())


def setup_api_key():
    """Load credentials for active backend (OpenRouter/OpenAI or Gemini)."""
    _load_env_file()

    if using_openai_backend():
        # OpenRouter is OpenAI-compatible.
        base_url = os.getenv("OPENAI_BASE_URL", "").strip() or os.getenv("OPENAI_API_BASE", "").strip()
        if not base_url:
            base_url = DEFAULT_OPENROUTER_BASE_URL
        os.environ["OPENAI_BASE_URL"] = base_url
        os.environ["OPENAI_API_BASE"] = base_url
        print(f"OpenAI/OpenRouter backend loaded. Model: {get_model_name()}")
        return

    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = input("Enter Google API Key: ")
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"
    print(f"Google backend loaded. Model: {DEFAULT_GEMINI_MODEL}")


_load_env_file()


# Allowed banking topics (used by topic_filter)
ALLOWED_TOPICS = [
    "banking", "account", "transaction", "transfer",
    "loan", "interest", "savings", "credit",
    "deposit", "withdrawal", "balance", "payment",
    "tai khoan", "giao dich", "tiet kiem", "lai suat",
    "chuyen tien", "the tin dung", "so du", "vay",
    "ngan hang", "atm",
]

# Blocked topics (immediate reject)
BLOCKED_TOPICS = [
    "hack", "exploit", "weapon", "drug", "illegal",
    "violence", "gambling", "bomb", "kill", "steal",
]
