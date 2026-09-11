from expense_tracker.cli import cli


class TestCLI:
    def test_cli_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "1.0.0" in result.output

    def test_cli_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Personal Expense Tracker" in result.output


class TestAddCommand:
    def test_add_expense(self, runner, temp_db):
        result = runner.invoke(cli, [
            "add",
            "--amount", "50.00",
            "--category", "Food",
            "--date", "2026-09-11",
            "--desc", "Lunch"
        ])
        assert result.exit_code == 0
        assert "Expense #1 added successfully" in result.output

    def test_add_expense_invalid_amount(self, runner, temp_db):
        result = runner.invoke(cli, [
            "add",
            "--amount", "abc",
            "--category", "Food",
            "--date", "2026-09-11"
        ])
        assert result.exit_code == 0
        assert "Error" in result.output

    def test_add_expense_invalid_date(self, runner, temp_db):
        result = runner.invoke(cli, [
            "add",
            "--amount", "50.00",
            "--category", "Food",
            "--date", "11-09-2026"
        ])
        assert result.exit_code == 0
        assert "Error" in result.output


class TestListCommand:
    def test_list_empty(self, runner, temp_db):
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "No expenses found" in result.output

    def test_list_with_expenses(self, runner, temp_db):
        runner.invoke(cli, [
            "add",
            "--amount", "50.00",
            "--category", "Food",
            "--date", "2026-09-11",
            "--desc", "Lunch"
        ])
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "Food" in result.output
        assert "$50.00" in result.output

    def test_list_by_month(self, runner, temp_db):
        runner.invoke(cli, [
            "add",
            "--amount", "50.00",
            "--category", "Food",
            "--date", "2026-09-11"
        ])
        runner.invoke(cli, [
            "add",
            "--amount", "25.00",
            "--category", "Transport",
            "--date", "2026-08-10"
        ])
        result = runner.invoke(cli, ["list", "--month", "2026-09"])
        assert result.exit_code == 0
        assert "Food" in result.output
        assert "Transport" not in result.output

    def test_list_by_category_id(self, runner, temp_db):
        runner.invoke(cli, [
            "add",
            "--amount", "50.00",
            "--category", "Food",
            "--date", "2026-09-11"
        ])
        runner.invoke(cli, [
            "add",
            "--amount", "25.00",
            "--category", "Transport",
            "--date", "2026-09-10"
        ])
        result = runner.invoke(cli, ["list", "--category", "1"])
        assert result.exit_code == 0
        assert "Food" in result.output
        assert "Transport" not in result.output


class TestEditCommand:
    def test_edit_expense(self, runner, temp_db):
        runner.invoke(cli, [
            "add",
            "--amount", "50.00",
            "--category", "Food",
            "--date", "2026-09-11",
            "--desc", "Lunch"
        ])
        result = runner.invoke(cli, [
            "edit", "1",
            "--amount", "45.00",
            "--desc", "Dinner"
        ])
        assert result.exit_code == 0
        assert "Expense #1 updated successfully" in result.output

    def test_edit_expense_not_found(self, runner, temp_db):
        result = runner.invoke(cli, [
            "edit", "999",
            "--amount", "45.00"
        ])
        assert result.exit_code == 0
        assert "Error" in result.output

    def test_edit_category_by_id(self, runner, temp_db):
        runner.invoke(cli, [
            "add",
            "--amount", "50.00",
            "--category", "Food",
            "--date", "2026-09-11"
        ])
        result = runner.invoke(cli, ["edit", "1", "--category", "2"])
        assert result.exit_code == 0
        assert "Expense #1 updated successfully" in result.output

    def test_edit_category_not_found(self, runner, temp_db):
        runner.invoke(cli, [
            "add",
            "--amount", "50.00",
            "--category", "Food",
            "--date", "2026-09-11"
        ])
        result = runner.invoke(cli, ["edit", "1", "--category", "999"])
        assert result.exit_code == 0
        assert "not found" in result.output


class TestDeleteCommand:
    def test_delete_expense(self, runner, temp_db):
        runner.invoke(cli, [
            "add",
            "--amount", "50.00",
            "--category", "Food",
            "--date", "2026-09-11"
        ])
        result = runner.invoke(cli, ["delete", "1", "--yes"])
        assert result.exit_code == 0
        assert "Expense #1 deleted successfully" in result.output

    def test_delete_expense_not_found(self, runner, temp_db):
        result = runner.invoke(cli, ["delete", "999", "--yes"])
        assert result.exit_code == 0
        assert "Error" in result.output


class TestSummaryCommand:
    def test_summary_empty(self, runner, temp_db):
        result = runner.invoke(cli, ["summary"])
        assert result.exit_code == 0
        assert "No expenses found" in result.output

    def test_summary_with_expenses(self, runner, temp_db):
        runner.invoke(cli, [
            "add",
            "--amount", "50.00",
            "--category", "Food",
            "--date", "2026-09-11"
        ])
        runner.invoke(cli, [
            "add",
            "--amount", "25.00",
            "--category", "Transport",
            "--date", "2026-09-10"
        ])
        result = runner.invoke(cli, ["summary"])
        assert result.exit_code == 0
        assert "Expense Summary" in result.output
        assert "Total: $75.00" in result.output


class TestCategoryCommand:
    def test_category_list(self, runner, temp_db):
        result = runner.invoke(cli, ["category", "list"])
        assert result.exit_code == 0
        assert "Food" in result.output
        assert "Transport" in result.output

    def test_category_add(self, runner, temp_db):
        result = runner.invoke(cli, ["category", "add", "--name", "Gym"])
        assert result.exit_code == 0
        assert "Category 'Gym' added successfully" in result.output

    def test_category_add_duplicate(self, runner, temp_db):
        runner.invoke(cli, ["category", "add", "--name", "Gym"])
        result = runner.invoke(cli, ["category", "add", "--name", "Gym"])
        assert result.exit_code == 0
        assert "already exists" in result.output
