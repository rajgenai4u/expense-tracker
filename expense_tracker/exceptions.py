"""Application-specific exceptions for the Expense Tracker."""


class ExpenseTrackerError(Exception):
    """Base class for all application errors."""


class DatabaseError(ExpenseTrackerError):
    """Raised when a database operation fails."""


class DuplicateCategoryError(ExpenseTrackerError):
    """Raised when attempting to add a category that already exists."""