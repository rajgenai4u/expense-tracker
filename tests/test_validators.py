import pytest
from expense_tracker.utils.validators import validate_amount, validate_date, validate_month


class TestValidateAmount:
    def test_valid_amount(self):
        assert validate_amount("50.00") == 50.00
        assert validate_amount("100") == 100.0
        assert validate_amount("0.01") == 0.01

    def test_invalid_amount_zero(self):
        with pytest.raises(ValueError, match="must be positive"):
            validate_amount("0")

    def test_invalid_amount_negative(self):
        with pytest.raises(ValueError, match="must be positive"):
            validate_amount("-50")

    def test_invalid_amount_string(self):
        with pytest.raises(ValueError, match="Invalid amount"):
            validate_amount("abc")

    def test_invalid_amount_empty(self):
        with pytest.raises(ValueError, match="Invalid amount"):
            validate_amount("")


class TestValidateDate:
    def test_valid_date(self):
        assert validate_date("2026-09-11") == "2026-09-11"
        assert validate_date("2024-12-31") == "2024-12-31"

    def test_invalid_date_format(self):
        with pytest.raises(ValueError, match="Invalid date format"):
            validate_date("11-09-2026")

    def test_invalid_date_format_slash(self):
        with pytest.raises(ValueError, match="Invalid date format"):
            validate_date("2026/09/11")

    def test_invalid_date_string(self):
        with pytest.raises(ValueError, match="Invalid date format"):
            validate_date("not-a-date")


class TestValidateMonth:
    def test_valid_month(self):
        assert validate_month("2026-09") == "2026-09"
        assert validate_month("2024-12") == "2024-12"

    def test_invalid_month_format(self):
        with pytest.raises(ValueError, match="Invalid month format"):
            validate_month("09-2026")

    def test_invalid_month_string(self):
        with pytest.raises(ValueError, match="Invalid month format"):
            validate_month("abc")

    def test_invalid_month_full_date(self):
        with pytest.raises(ValueError, match="Invalid month format"):
            validate_month("2026-09-11")
