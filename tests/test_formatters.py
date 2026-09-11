import pytest
from expense_tracker.utils.formatters import format_currency, format_date, format_table


class TestFormatCurrency:
    def test_format_currency(self):
        assert format_currency(50.0) == "$50.00"
        assert format_currency(100) == "$100.00"
        assert format_currency(1234.56) == "$1,234.56"
        assert format_currency(0.01) == "$0.01"

    def test_format_currency_large_amount(self):
        assert format_currency(1000000) == "$1,000,000.00"

    def test_format_currency_zero(self):
        assert format_currency(0) == "$0.00"


class TestFormatDate:
    def test_format_date(self):
        assert format_date("2026-09-11") == "Sep 11, 2026"
        assert format_date("2024-12-31") == "Dec 31, 2024"

    def test_format_date_invalid(self):
        assert format_date("invalid") == "invalid"
        assert format_date("2026/09/11") == "2026/09/11"


class TestFormatTable:
    def test_format_table(self):
        headers = ["ID", "Name", "Amount"]
        rows = [
            [1, "Food", "$50.00"],
            [2, "Transport", "$25.00"],
        ]
        result = format_table(headers, rows)
        assert "ID" in result
        assert "Name" in result
        assert "Amount" in result
        assert "Food" in result
        assert "Transport" in result

    def test_format_table_empty(self):
        headers = ["ID", "Name"]
        rows = []
        result = format_table(headers, rows)
        assert "ID" in result
        assert "Name" in result
