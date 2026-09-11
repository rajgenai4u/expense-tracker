from datetime import datetime
from expense_tracker.config import DATE_FORMAT


def validate_amount(amount_str: str) -> float:
    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid amount: {amount_str}")

    if amount <= 0:
        raise ValueError(f"Amount must be positive, got: {amount}")
    return amount


def validate_date(date_str: str) -> str:
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return date_str
    except ValueError:
        raise ValueError(f"Invalid date format. Use {DATE_FORMAT}")


def validate_month(month_str: str) -> str:
    try:
        datetime.strptime(month_str, "%Y-%m")
        return month_str
    except ValueError:
        raise ValueError(f"Invalid month format. Use YYYY-MM")
