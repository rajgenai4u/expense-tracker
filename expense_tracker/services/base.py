import sqlite3
import logging
from functools import wraps
from expense_tracker.database import get_connection
from expense_tracker.exceptions import DatabaseError

logger = logging.getLogger(__name__)


def handle_db_errors(func):
    """Wrap a service method, translating low-level DB failures into DatabaseError."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except sqlite3.Error as e:
            if self.conn is not None:
                try:
                    self.conn.rollback()
                except sqlite3.Error:
                    pass
            logger.error("Database operation failed: %s", e)
            raise DatabaseError(f"Database operation failed: {e}") from e

    return wrapper


class BaseService:
    """Shared connection lifecycle and error handling for all services."""

    def __init__(self):
        self.conn = get_connection()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None