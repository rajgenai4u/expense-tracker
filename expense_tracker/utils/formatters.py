from datetime import datetime
from expense_tracker.config import CURRENCY_SYMBOL, DATE_FORMAT


def format_currency(amount: float) -> str:
    return f"{CURRENCY_SYMBOL}{amount:,.2f}"


def format_date(date_str: str) -> str:
    try:
        date_obj = datetime.strptime(date_str, DATE_FORMAT)
        return date_obj.strftime("%b %d, %Y")
    except ValueError:
        return date_str


def format_table(headers: list[str], rows: list[list]) -> str:
    from tabulate import tabulate
    return tabulate(rows, headers=headers, tablefmt="grid")
