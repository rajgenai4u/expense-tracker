"""Logging configuration for the Expense Tracker."""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

from expense_tracker import config

DEFAULT_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

_configured = False


def get_package_logger(name: str = "") -> logging.Logger:
    """Return a logger scoped to the expense_tracker package."""
    if name:
        return logging.getLogger(f"expense_tracker.{name}")
    return logging.getLogger("expense_tracker")


def setup_logging(level: int = logging.INFO, log_file: Path = None) -> None:
    """Configure package logging with a console handler and a rotating file handler.

    The console shows INFO and above; the file captures DEBUG detail. Idempotent.
    """
    global _configured
    if _configured:
        return

    logger = get_package_logger()
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = logging.Formatter(DEFAULT_FORMAT)

    console = logging.StreamHandler(sys.stderr)
    console.setLevel(level)
    console.setFormatter(formatter)
    logger.addHandler(console)

    log_file = log_file or config.LOG_PATH
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            str(log_file),
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError as e:
        logger.warning("Could not create log file %s: %s", log_file, e)

    _configured = True


def reset_logging() -> None:
    """Remove all handlers from the package logger (used mainly by tests)."""
    global _configured
    logger = get_package_logger()
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()
    logger.propagate = True
    _configured = False