import sqlite3
import logging
from expense_tracker.services.base import BaseService, handle_db_errors
from expense_tracker.models.category import Category
from expense_tracker.exceptions import DuplicateCategoryError

logger = logging.getLogger(__name__)


class CategoryService(BaseService):
    @handle_db_errors
    def list_categories(self) -> list[Category]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM categories ORDER BY name")
        rows = cursor.fetchall()
        return [self._from_row(row) for row in rows]

    @handle_db_errors
    def get_category(self, category_id: int) -> Category | None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = cursor.fetchone()
        return self._from_row(row) if row else None

    @handle_db_errors
    def get_category_by_name(self, name: str) -> Category | None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM categories WHERE name = ?", (name,))
        row = cursor.fetchone()
        return self._from_row(row) if row else None

    @handle_db_errors
    def add_category(self, name: str) -> int:
        if self.get_category_by_name(name):
            logger.warning("Duplicate category attempted: '%s'", name)
            raise DuplicateCategoryError(f"Category '{name}' already exists")
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            self.conn.commit()
            logger.debug("Added category id=%s name='%s'", cursor.lastrowid, name)
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            logger.warning("Duplicate category attempted: '%s'", name)
            raise DuplicateCategoryError(f"Category '{name}' already exists")

    @handle_db_errors
    def delete_category(self, category_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        self.conn.commit()
        deleted = cursor.rowcount > 0
        logger.debug("Deleted category id=%s (deleted=%s)", category_id, deleted)
        return deleted

    @staticmethod
    def _from_row(row) -> Category:
        return Category(id=row["id"], name=row["name"])