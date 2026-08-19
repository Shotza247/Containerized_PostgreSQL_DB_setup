import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
SCHEMA_DIR = DATABASE_DIR / "schema"
SEED_DIR = DATABASE_DIR / "seed"
DEV_DIR = DATABASE_DIR / "dev"

load_dotenv(BASE_DIR / ".env")


def _get_port() -> int:
    value = os.getenv("DB_PORT", "5432")
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError("DB_PORT must be a number.") from exc


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": _get_port(),
    "database": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}


def validate_db_config(db_config: dict) -> None:
    missing = [key for key, value in db_config.items() if value in (None, "")]
    if missing:
        names = ", ".join(missing)
        raise ValueError(f"Missing database config value(s): {names}")
