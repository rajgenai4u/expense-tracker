import pytest
import expense_tracker.database as database
from expense_tracker import config
from expense_tracker.exceptions import DatabaseError, DuplicateCategoryError
from expense_tracker.database import get_connection
from expense_tracker.services.category_service import CategoryService
from expense_tracker.services.expense_service import ExpenseService
from click.testing import CliRunner
from expense_tracker.cli import cli


class TestCustomExceptions:
    def test_database_error_is_expense_tracker_error(self):
        assert issubclass(DatabaseError, Exception)

    def test_duplicate_category_error_is_expense_tracker_error(self):
        assert issubclass(DuplicateCategoryError, Exception)


class TestDatabaseErrorHandling:
    def test_get_connection_failure_raises_database_error(self, monkeypatch, tmp_path):
        blocking_file = tmp_path / "not_a_dir"
        blocking_file.write_text("I am a file, not a directory")
        monkeypatch.setattr(config, "DB_PATH", tmp_path / "db")
        monkeypatch.setattr(config, "DATA_DIR", blocking_file)
        with pytest.raises(DatabaseError):
            get_connection()


class TestServiceErrorWrapping:
    def test_expense_service_database_error(self, temp_db):
        svc = ExpenseService()
        with pytest.raises(DatabaseError):
            svc.add_expense(amount=10.0, category_id=9999, date="2026-09-11")
        svc.close()

    def test_category_service_duplicate_raises_custom_error(self, temp_db):
        cat_service = CategoryService()
        with pytest.raises(DuplicateCategoryError):
            cat_service.add_category("Food")
        cat_service.close()


class TestCLIErrorHandling:
    def test_cli_db_error_shows_friendly_message(self, runner, monkeypatch, tmp_path):
        monkeypatch.setattr(config, "DB_PATH", tmp_path / "db")
        monkeypatch.setattr(config, "DATA_DIR", tmp_path)

        def _boom(*args, **kwargs):
            raise DatabaseError("Unable to open database: locked")

        monkeypatch.setattr(database, "get_connection", _boom)
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 1
        assert "Unable to open database" in result.output

    def test_cli_duplicate_category_friendly_message(self, runner, temp_db):
        result = runner.invoke(cli, ["category", "add", "--name", "Food"])
        assert result.exit_code == 0
        assert "already exists" in result.output
        assert "Traceback" not in result.output

    def test_cli_unexpected_error_shows_friendly_message(self, runner, temp_db, monkeypatch):
        def _boom(*args, **kwargs):
            raise RuntimeError("unexpected boom")

        monkeypatch.setattr(CategoryService, "list_categories", _boom)
        result = runner.invoke(cli, ["category", "list"])
        assert result.exit_code == 0
        assert "Unexpected error" in result.output
        assert "Traceback" not in result.output


class TestConnectionCleanup:
    def test_service_context_manager_closes_connection(self, temp_db):
        with CategoryService() as cat_service:
            assert cat_service.conn is not None
        assert cat_service.conn is None

    def test_services_close_idempotent(self, temp_db):
        exp_service = ExpenseService()
        exp_service.close()
        exp_service.close()