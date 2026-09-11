import logging
from expense_tracker.logging_config import (
    setup_logging,
    reset_logging,
    get_package_logger,
)


class TestLoggingConfiguration:
    def teardown_method(self):
        reset_logging()

    def test_setup_logging_adds_handlers(self, tmp_path):
        setup_logging(log_file=tmp_path / "app.log")
        logger = get_package_logger()
        handler_types = {type(h) for h in logger.handlers}
        assert logging.StreamHandler in handler_types
        assert logging.handlers.RotatingFileHandler in handler_types

    def test_setup_logging_is_idempotent(self, tmp_path):
        logger = get_package_logger()
        before = len(logger.handlers)
        setup_logging(log_file=tmp_path / "app.log")
        after_first = len(logger.handlers)
        assert after_first == before + 2

        setup_logging(log_file=tmp_path / "app.log")
        assert len(logger.handlers) == after_first

    def test_logging_writes_to_file(self, tmp_path):
        log_file = tmp_path / "app.log"
        setup_logging(level=logging.DEBUG, log_file=log_file)
        test_logger = get_package_logger("test")
        test_logger.info("ALERT info message")
        test_logger.debug("ALERT debug message")
        content = log_file.read_text()
        assert "ALERT info message" in content
        assert "ALERT debug message" in content

    def test_reset_logging_removes_handlers(self, tmp_path):
        setup_logging(log_file=tmp_path / "app.log")
        reset_logging()
        assert get_package_logger().handlers == []

    def test_console_level_filters_debug(self, capsys, tmp_path):
        log_file = tmp_path / "app.log"
        setup_logging(level=logging.INFO, log_file=log_file)
        test_logger = get_package_logger("capsys_test")
        test_logger.debug("ALERT hidden from console")
        test_logger.info("ALERT shown on console")
        captured = capsys.readouterr()
        assert "ALERT shown on console" in captured.err
        assert "ALERT hidden from console" not in captured.err
        assert "ALERT hidden from console" in log_file.read_text()