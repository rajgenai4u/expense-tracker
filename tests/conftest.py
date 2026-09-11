import pytest
import tempfile
import logging
from pathlib import Path
from click.testing import CliRunner
from expense_tracker import config
from expense_tracker.database import initialize_db


@pytest.fixture(autouse=True)
def _silence_logging(monkeypatch):
    """Keep test output clean by disabling logging during tests."""
    monkeypatch.setattr("expense_tracker.logging_config.setup_logging", lambda **kwargs: None)
    logger = logging.getLogger("expense_tracker")
    logger.addHandler(logging.NullHandler())
    logger.setLevel(logging.CRITICAL)
    yield


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


@pytest.fixture
def temp_db():
    """Create an isolated temporary database for each test."""
    original_db_path = config.DB_PATH
    original_data_dir = config.DATA_DIR

    with tempfile.TemporaryDirectory() as tmpdir:
        config.DB_PATH = Path(tmpdir) / "test_expenses.db"
        config.DATA_DIR = Path(tmpdir)
        initialize_db()
        yield
        config.DB_PATH = original_db_path
        config.DATA_DIR = original_data_dir