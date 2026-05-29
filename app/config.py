import os
from dotenv import load_dotenv

load_dotenv()


def _require(key):
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Variable de entorno requerida no encontrada: '{key}'. "
            f"Revisa tu archivo .env."
        )
    return value


def _optional(key, default=None):
    return os.getenv(key, default)


# ------------------------------------------------------------
# LLM
# ------------------------------------------------------------

LLM_PROVIDER = _optional("LLM_PROVIDER", "groq")
LLM_MODEL = _optional("LLM_MODEL", "llama3-8b-8192")

OPENAI_API_KEY = _optional("OPENAI_API_KEY")
GROQ_API_KEY = _optional("GROQ_API_KEY")
ANTHROPIC_API_KEY = _optional("ANTHROPIC_API_KEY")


# ------------------------------------------------------------
# BASE DE DATOS VECTORIAL
# ------------------------------------------------------------

CHROMA_PATH = _optional("CHROMA_PATH", "./chroma_db")
CHROMA_COLLECTION = _optional("CHROMA_COLLECTION", "architecture_knowledge")


# ------------------------------------------------------------
# EMBEDDINGS
# ------------------------------------------------------------

EMBEDDING_MODEL = _optional("EMBEDDING_MODEL", "all-MiniLM-L6-v2")


# ------------------------------------------------------------
# INGESTA / GITHUB
# ------------------------------------------------------------

REPO_URL = _optional("REPO_URL", "")
LOCAL_REPO = _optional("LOCAL_REPO", "./repos/project")


# ------------------------------------------------------------
# CHUNKING
# ------------------------------------------------------------

CHUNK_SIZE = int(_optional("CHUNK_SIZE", "1500"))
CHUNK_OVERLAP = int(_optional("CHUNK_OVERLAP", "150"))


# ------------------------------------------------------------
# INTERFAZ
# ------------------------------------------------------------

STREAMLIT_PORT = int(_optional("STREAMLIT_PORT", "8501"))


# ------------------------------------------------------------
# VOZ OPCIONAL
# ------------------------------------------------------------

WHISPER_MODEL = _optional("WHISPER_MODEL", "base")
TTS_LANGUAGE = _optional("TTS_LANGUAGE", "es")