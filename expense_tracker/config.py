import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "expenses.db"
LOG_DIR = DATA_DIR / "logs"
LOG_PATH = LOG_DIR / "expense-tracker.log"

DATE_FORMAT = "%Y-%m-%d"
CURRENCY_SYMBOL = "$"

DEFAULT_CATEGORIES = [
    "Food",
    "Transport",
    "Entertainment",
    "Utilities",
    "Shopping",
    "Health",
    "Education",
    "Other",
]
