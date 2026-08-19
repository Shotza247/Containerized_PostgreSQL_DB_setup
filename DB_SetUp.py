from contextlib import contextmanager
from pathlib import Path
from typing import Iterable

import psycopg2
from psycopg2.extensions import connection as PsycopgConnection

from config import DB_CONFIG, SCHEMA_DIR, SEED_DIR, validate_db_config
from logging_config import logger


class PostgresDB:
    """Small reusable wrapper for PostgreSQL connections and setup scripts."""

    def __init__(self, db_config: dict | None = None) -> None:
        self.db_config = db_config or DB_CONFIG

    def connect(self) -> PsycopgConnection:
        validate_db_config(self.db_config)
        logger.info(
            "Connecting to PostgreSQL at %s:%s/%s",
            self.db_config["host"],
            self.db_config["port"],
            self.db_config["database"],
        )
        return psycopg2.connect(**self.db_config)

    @contextmanager
    def connection(self) -> Iterable[PsycopgConnection]:
        connection = self.connect()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            logger.exception("Database operation failed.")
            raise
        finally:
            connection.close()
            logger.info("Connection closed.")

    def check_connection(self) -> str:
        with self.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]

        logger.info("Connected to PostgreSQL: %s", version)
        return version

    def execute_sql(self, sql: str) -> None:
        if not sql.strip():
            return

        with self.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)

    def execute_file(self, file_path: str | Path) -> None:
        path = Path(file_path)
        logger.info("Running SQL file: %s", path)
        self.execute_sql(path.read_text(encoding="utf-8"))

    def execute_directory(self, directory: str | Path) -> None:
        path = Path(directory)
        if not path.exists():
            raise FileNotFoundError(f"SQL directory does not exist: {path}")

        sql_files = sorted(path.glob("*.sql"))
        if not sql_files:
            logger.warning("No SQL files found in %s", path)
            return

        for sql_file in sql_files:
            self.execute_file(sql_file)

    def init_schema(self, schema_dir: str | Path = SCHEMA_DIR) -> None:
        self.execute_directory(schema_dir)

    def seed(self, seed_dir: str | Path = SEED_DIR) -> None:
        self.execute_directory(seed_dir)


def connect(db_config: dict | None = None) -> PsycopgConnection:
    """Backward-compatible raw connection helper for existing repositories."""
    return PostgresDB(db_config).connect()


@contextmanager
def get_connection(db_config: dict | None = None) -> Iterable[PsycopgConnection]:
    """Context-managed connection that commits or rolls back automatically."""
    with PostgresDB(db_config).connection() as connection:
        yield connection


def check_connection(db_config: dict | None = None) -> str:
    return PostgresDB(db_config).check_connection()


def initialize_database(
    schema_dir: str | Path = SCHEMA_DIR,
    seed_dir: str | Path = SEED_DIR,
    with_seed: bool = False,
    db_config: dict | None = None,
) -> None:
    db = PostgresDB(db_config)
    db.init_schema(schema_dir)

    if with_seed:
        db.seed(seed_dir)
