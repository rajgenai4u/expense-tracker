import sqlite3
import logging
from contextlib import contextmanager
from expense_tracker import config
from expense_tracker.config import DEFAULT_CATEGORIES
from expense_tracker.exceptions import DatabaseError

logger = logging.getLogger(__name__)


def get_connection() -> sqlite3.Connection:
    try:
        config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(config.DB_PATH), timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        logger.debug("Opened database connection to %s", config.DB_PATH)
        return conn
    except (sqlite3.Error, OSError) as e:
        logger.error("Failed to open database %s: %s", config.DB_PATH, e)
        raise DatabaseError(f"Unable to open database: {e}") from e


@contextmanager
def db_session():
    """Context manager that yields a connection and guarantees cleanup."""
    conn = get_connection()
    try:
        yield conn
    except sqlite3.Error as e:
        conn.rollback()
        logger.warning("Database operation rolled back: %s", e)
        raise DatabaseError(f"Database operation failed: {e}") from e
    finally:
        conn.close()
        logger.debug("Closed database connection to %s", config.DB_PATH)


def initialize_db() -> None:
    try:
        with db_session() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    category_id INTEGER,
                    date TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            """)

            cursor.execute("SELECT COUNT(*) as count FROM categories")
            if cursor.fetchone()["count"] == 0:
                logger.debug("Seeding %d default categories", len(DEFAULT_CATEGORIES))
                cursor.executemany(
                    "INSERT INTO categories (name) VALUES (?)",
                    [(name,) for name in DEFAULT_CATEGORIES],
                )

            conn.commit()
        logger.info("Database initialized at %s", config.DB_PATH)
    except sqlite3.Error as e:
        logger.error("Failed to initialize database: %s", e)
        raise DatabaseError(f"Failed to initialize database: {e}") from e