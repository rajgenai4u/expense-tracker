import logging
from datetime import datetime
from expense_tracker.services.base import BaseService, handle_db_errors
from expense_tracker.models.expense import Expense

logger = logging.getLogger(__name__)


class ExpenseService(BaseService):
    @handle_db_errors
    def add_expense(self, amount: float, category_id: int, date: str, description: str = "") -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (amount, category_id, date, description) VALUES (?, ?, ?, ?)",
            (amount, category_id, date, description),
        )
        self.conn.commit()
        expense_id = cursor.lastrowid
        logger.debug("Added expense id=%s amount=%s date=%s", expense_id, amount, date)
        return expense_id

    @handle_db_errors
    def get_expense(self, expense_id: int) -> Expense | None:
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT e.*, c.name as category_name
               FROM expenses e
               LEFT JOIN categories c ON e.category_id = c.id
               WHERE e.id = ?""",
            (expense_id,),
        )
        row = cursor.fetchone()
        return self._from_row(row) if row else None

    @handle_db_errors
    def list_expenses(self, month: str = None, category_id: int = None) -> list[Expense]:
        query = """
            SELECT e.*, c.name as category_name
            FROM expenses e
            LEFT JOIN categories c ON e.category_id = c.id
            WHERE 1=1
        """
        params: list = []

        if month:
            query += " AND e.date LIKE ?"
            params.append(f"{month}%")

        if category_id:
            query += " AND e.category_id = ?"
            params.append(category_id)

        query += " ORDER BY e.date DESC"

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        logger.debug("Listed %d expenses (month=%s, category_id=%s)", len(rows), month, category_id)
        return [self._from_row(row) for row in rows]

    @handle_db_errors
    def update_expense(self, expense_id: int, amount: float = None, category_id: int = None,
                       date: str = None, description: str = None) -> bool:
        updates = []
        params = []

        if amount is not None:
            updates.append("amount = ?")
            params.append(amount)
        if category_id is not None:
            updates.append("category_id = ?")
            params.append(category_id)
        if date is not None:
            updates.append("date = ?")
            params.append(date)
        if description is not None:
            updates.append("description = ?")
            params.append(description)

        if not updates:
            return False

        params.append(expense_id)
        query = f"UPDATE expenses SET {', '.join(updates)} WHERE id = ?"

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        updated = cursor.rowcount > 0
        logger.debug("Updated expense id=%s (updated=%s)", expense_id, updated)
        return updated

    @handle_db_errors
    def delete_expense(self, expense_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()
        deleted = cursor.rowcount > 0
        logger.debug("Deleted expense id=%s (deleted=%s)", expense_id, deleted)
        return deleted

    @handle_db_errors
    def get_monthly_summary(self, month: str = None) -> dict:
        if not month:
            month = datetime.now().strftime("%Y-%m")

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.name, SUM(e.amount) as total
            FROM expenses e
            LEFT JOIN categories c ON e.category_id = c.id
            WHERE e.date LIKE ?
            GROUP BY c.name
            ORDER BY total DESC
        """, (f"{month}%",))

        summary = {}
        for row in cursor.fetchall():
            summary[row["name"] or "Uncategorized"] = row["total"]

        summary["total"] = sum(summary.values())
        summary["month"] = month
        logger.debug("Monthly summary for %s: total=%s across %d categories", month, summary["total"], len(summary) - 2)
        return summary

    @staticmethod
    def _from_row(row) -> Expense:
        return Expense(
            id=row["id"],
            amount=row["amount"],
            category_id=row["category_id"],
            category_name=row["category_name"],
            date=row["date"],
            description=row["description"],
            created_at=row["created_at"],
        )