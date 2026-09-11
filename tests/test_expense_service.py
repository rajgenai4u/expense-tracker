import pytest
from expense_tracker.services.expense_service import ExpenseService


class TestExpenseService:
    def test_add_expense(self, temp_db):
        exp_service = ExpenseService()
        expense_id = exp_service.add_expense(
            amount=50.00,
            category_id=1,
            date="2026-09-11",
            description="Lunch"
        )
        exp_service.close()
        assert expense_id is not None
        assert expense_id > 0

    def test_get_expense(self, temp_db):
        exp_service = ExpenseService()
        expense_id = exp_service.add_expense(
            amount=25.00,
            category_id=2,
            date="2026-09-10",
            description="Bus fare"
        )
        expense = exp_service.get_expense(expense_id)
        exp_service.close()
        assert expense is not None
        assert expense.amount == 25.00
        assert expense.category_name == "Transport"
        assert expense.date == "2026-09-10"

    def test_get_expense_not_found(self, temp_db):
        exp_service = ExpenseService()
        expense = exp_service.get_expense(999)
        exp_service.close()
        assert expense is None

    def test_list_expenses(self, temp_db):
        exp_service = ExpenseService()
        exp_service.add_expense(50.00, 1, "2026-09-11", "Food")
        exp_service.add_expense(25.00, 2, "2026-09-10", "Transport")
        expenses = exp_service.list_expenses()
        exp_service.close()
        assert len(expenses) == 2

    def test_list_expenses_by_month(self, temp_db):
        exp_service = ExpenseService()
        exp_service.add_expense(50.00, 1, "2026-09-11", "Food")
        exp_service.add_expense(25.00, 2, "2026-08-10", "Transport")
        expenses = exp_service.list_expenses(month="2026-09")
        exp_service.close()
        assert len(expenses) == 1
        assert expenses[0].date == "2026-09-11"

    def test_list_expenses_by_category(self, temp_db):
        exp_service = ExpenseService()
        exp_service.add_expense(50.00, 1, "2026-09-11", "Food")
        exp_service.add_expense(25.00, 2, "2026-09-10", "Transport")
        expenses = exp_service.list_expenses(category_id=1)
        exp_service.close()
        assert len(expenses) == 1
        assert expenses[0].category_name == "Food"

    def test_update_expense(self, temp_db):
        exp_service = ExpenseService()
        expense_id = exp_service.add_expense(50.00, 1, "2026-09-11", "Food")
        result = exp_service.update_expense(expense_id, amount=45.00)
        expense = exp_service.get_expense(expense_id)
        exp_service.close()
        assert result is True
        assert expense.amount == 45.00

    def test_update_expense_not_found(self, temp_db):
        exp_service = ExpenseService()
        result = exp_service.update_expense(999, amount=45.00)
        exp_service.close()
        assert result is False

    def test_delete_expense(self, temp_db):
        exp_service = ExpenseService()
        expense_id = exp_service.add_expense(50.00, 1, "2026-09-11", "Food")
        result = exp_service.delete_expense(expense_id)
        expense = exp_service.get_expense(expense_id)
        exp_service.close()
        assert result is True
        assert expense is None

    def test_delete_expense_not_found(self, temp_db):
        exp_service = ExpenseService()
        result = exp_service.delete_expense(999)
        exp_service.close()
        assert result is False

    def test_get_monthly_summary(self, temp_db):
        exp_service = ExpenseService()
        exp_service.add_expense(50.00, 1, "2026-09-11", "Food")
        exp_service.add_expense(25.00, 2, "2026-09-10", "Transport")
        summary = exp_service.get_monthly_summary("2026-09")
        exp_service.close()
        assert summary["total"] == 75.00
        assert summary["Food"] == 50.00
        assert summary["Transport"] == 25.00

    def test_get_monthly_summary_empty(self, temp_db):
        exp_service = ExpenseService()
        summary = exp_service.get_monthly_summary("2026-01")
        exp_service.close()
        assert summary["total"] == 0
