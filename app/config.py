import os
from dotenv import load_dotenv

load_dotenv()


def _require(key):
    """Lanza un error claro si una variable obligatoria no está definida."""
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Variable de entorno requerida no encontrada: '{key}'\n"
            f"Asegúrate de copiar .env.example como .env y rellenar el valor."
        )
    return value


def _optional(key, default=None):
    return os.getenv(key, default)


# ------------------------------------------------------------
# LLM
# ------------------------------------------------------------

LLM_PROVIDER   = _require("LLM_PROVIDER")      # groq | openai | anthropic
LLM_MODEL      = _require("LLM_MODEL")

OPENAI_API_KEY    = _optional("OPENAI_API_KEY")
GROQ_API_KEY      = _optional("GROQ_API_KEY")
ANTHROPIC_API_KEY = _optional("ANTHROPIC_API_KEY")

# Validar que la key del proveedor elegido esté presente
_PROVIDER_KEYS = {
    "openai":    OPENAI_API_KEY,
    "groq":      GROQ_API_KEY,
    "anthropic": ANTHROPIC_API_KEY,
}

if not _PROVIDER_KEYS.get(LLM_PROVIDER.lower()):
    raise EnvironmentError(
        f"Proveedor '{LLM_PROVIDER}' seleccionado pero su API key no está definida.\n"
        f"Define la variable correspondiente en tu archivo .env."
    )


# ------------------------------------------------------------
# BASE DE DATOS VECTORIAL
# ------------------------------------------------------------

CHROMA_PATH       = _optional("CHROMA_PATH", "./chroma_db")
CHROMA_COLLECTION = _optional("CHROMA_COLLECTION", "rag_arquitecto")


# ------------------------------------------------------------
# EMBEDDINGS
# ------------------------------------------------------------

EMBEDDING_MODEL = _optional("EMBEDDING_MODEL", "all-MiniLM-L6-v2")


# ------------------------------------------------------------
# INGESTA
# ------------------------------------------------------------

REPO_URL   = _optional("REPO_URL", "")
LOCAL_REPO = _optional("LOCAL_REPO", "./repos/project")


# ------------------------------------------------------------
# CHUNKING
# ------------------------------------------------------------

CHUNK_SIZE    = int(_optional("CHUNK_SIZE", "1500"))
CHUNK_OVERLAP = int(_optional("CHUNK_OVERLAP", "150"))


# ------------------------------------------------------------
# INTERFAZ
# ------------------------------------------------------------

STREAMLIT_PORT = int(_optional("STREAMLIT_PORT", "8501"))


# ------------------------------------------------------------
# VOZ (OPCIONAL)
# ------------------------------------------------------------

WHISPER_MODEL = _optional("WHISPER_MODEL", "base")
TTS_LANGUAGE  = _optional("TTS_LANGUAGE", "es")
