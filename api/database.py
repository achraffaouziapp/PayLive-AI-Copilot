from pathlib import Path
from typing import Any, Dict, List, Optional
import logging
import os

import psycopg2
from psycopg2.extras import RealDictCursor


try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


# -------------------------------------------------------------------
# PostgreSQL database access layer
# -------------------------------------------------------------------
# This module centralizes the PostgreSQL connection and query helpers
# used by the FastAPI application.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[1]


def load_environment_variables() -> None:
    """
    Load environment variables from .env if available.
    """
    env_path = BASE_DIR / ".env"

    if load_dotenv is not None and env_path.exists():
        load_dotenv(env_path)


def get_database_config() -> Dict[str, Any]:
    """
    Return PostgreSQL connection configuration.

    Default values are compatible with the Docker Compose setup.
    """
    load_environment_variables()

    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", "5433")),
        "dbname": os.getenv("POSTGRES_DB", "paylive_ai_copilot"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    }


def get_connection():
    """
    Create and return a PostgreSQL connection.
    """
    config = get_database_config()

    return psycopg2.connect(
        **config,
        cursor_factory=RealDictCursor,
    )


def fetch_all(query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """
    Execute a SELECT query and return all rows as dictionaries.
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def fetch_one(query: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
    """
    Execute a SELECT query and return one row as a dictionary.
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()


def check_database_connection() -> Dict[str, Any]:
    """
    Check if the database connection is available.
    """
    try:
        row = fetch_one("SELECT current_database() AS database_name, version() AS postgres_version;")

        return {
            "database_available": True,
            "database_name": row["database_name"] if row else None,
            "postgres_version": row["postgres_version"] if row else None,
        }

    except Exception as error:
        logging.exception("Database connection check failed.")

        return {
            "database_available": False,
            "database_name": None,
            "postgres_version": None,
            "error": str(error),
        }