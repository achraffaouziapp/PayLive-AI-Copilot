from pathlib import Path
import os

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader


try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


# -------------------------------------------------------------------
# API key security
# -------------------------------------------------------------------
# This module protects API endpoints with a simple API key mechanism.
#
# The expected key is read from the API_KEY environment variable.
# Clients must send it through the X-API-Key HTTP header.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[1]

API_KEY_HEADER_NAME = "X-API-Key"

api_key_header = APIKeyHeader(
    name=API_KEY_HEADER_NAME,
    auto_error=False,
)


def load_environment_variables() -> None:
    """
    Load environment variables from .env if available.
    """
    env_path = BASE_DIR / ".env"

    if load_dotenv is not None and env_path.exists():
        load_dotenv(env_path)


def get_expected_api_key() -> str:
    """
    Return the expected API key.
    """
    load_environment_variables()

    return os.getenv("API_KEY", "paylive-dev-api-key")


async def require_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Validate the API key from the request header.
    """
    expected_api_key = get_expected_api_key()

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Please provide the X-API-Key header.",
        )

    if api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key.",
        )

    return api_key