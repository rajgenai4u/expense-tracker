import sqlite3
import logging
import click
from datetime import datetime
from functools import wraps
from expense_tracker.database import initialize_db
from expense_tracker.services.expense_service import ExpenseService
from expense_tracker.services.category_service import CategoryService
from expense_tracker.utils.formatters import format_currency, format_date, format_table
from expense_tracker.utils.validators import validate_amount, validate_date, validate_month
from expense_tracker.config import DATE_FORMAT
from expense_tracker.exceptions import ExpenseTrackerError
from expense_tracker.logging_config import setup_logging

logger = logging.getLogger(__name__)

EXPENSE_HEADERS = ["ID", "Date", "Category", "Amount", "Description"]


def handle_errors(func):
    """Decorator that catches known and unexpected errors and prints friendly messages."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug("Invoking command: %s", func.__name__)
        try:
            return func(*args, **kwargs)
        except click.exceptions.Abort:
            raise
        except (ExpenseTrackerError, sqlite3.Error) as e:
            logger.error("Command '%s' failed: %s", func.__name__, e)
            click.echo(f"Error: {e}", err=True)
        except Exception as e:
            logger.error("Command '%s' raised unhandled error: %s", func.__name__, e)
            logger.debug("Full traceback for '%s':", func.__name__, exc_info=True)
            click.echo(f"Unexpected error: {e}", err=True)
    return wrapper


def fail(message):
    """Print a user-facing error and signal early return from a command."""
    click.echo(f"Error: {message}", err=True)
    return False


def parse_or_fail(validator, value):
    """Validate a value, printing an error and returning None if invalid."""
    try:
        return validator(value)
    except ValueError as e:
        fail(str(e))
        return None


def resolve_category(cat_service: CategoryService, category: str):
    """Resolve a category by name or numeric ID, returning None if not found."""
    cat = cat_service.get_category_by_name(category)
    if cat:
        return cat

    try:
        return cat_service.get_category(int(category))
    except (ValueError, TypeError):
        return None


def expense_rows(expenses):
    """Build table rows from a list of expenses."""
    return [
        [
            exp.id,
            format_date(exp.date),
            exp.category_name,
            format_currency(exp.amount),
            exp.description or "-",
        ]
        for exp in expenses
    ]


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Personal Expense Tracker - Track your expenses from the command line."""
    setup_logging()
    try:
        initialize_db()
    except ExpenseTrackerError as e:
        logger.error("Database initialization failed: %s", e)
        raise click.ClickException(str(e))


@cli.command()
@click.option("--amount", "-a", required=True, help="Expense amount")
@click.option("--category", "-c", required=True, help="Category name or ID")
@click.option("--date", "-d", default=datetime.now().strftime(DATE_FORMAT), help="Date (YYYY-MM-DD)")
@click.option("--desc", default="", help="Description")
@handle_errors
def add(amount, category, date, desc):
    """Add a new expense."""
    amount = parse_or_fail(validate_amount, amount)
    date = parse_or_fail(validate_date, date)
    if amount is None or date is None:
        return

    with ExpenseService() as exp_service, CategoryService() as cat_service:
        cat = resolve_category(cat_service, category)
        if not cat:
            return fail(f"Category '{category}' not found.")

        expense_id = exp_service.add_expense(amount, cat.id, date, desc)
        click.echo(f"Expense #{expense_id} added successfully.")


@cli.command()
@click.option("--month", "-m", help="Filter by month (YYYY-MM)")
@click.option("--category", "-c", help="Filter by category name or ID")
@handle_errors
def list(month, category):
    """List expenses with optional filters."""
    with ExpenseService() as exp_service, CategoryService() as cat_service:
        category_id = None
        if category:
            cat = resolve_category(cat_service, category)
            if not cat:
                return fail(f"Category '{category}' not found.")
            category_id = cat.id

        validated_month = parse_or_fail(validate_month, month) if month else None
        if month and validated_month is None:
            return

        expenses = exp_service.list_expenses(month=validated_month, category_id=category_id)

        if not expenses:
            click.echo("No expenses found.")
            return

        click.echo(format_table(EXPENSE_HEADERS, expense_rows(expenses)))


@cli.command()
@click.argument("expense_id", type=int)
@click.option("--amount", "-a", help="New amount")
@click.option("--category", "-c", help="New category name or ID")
@click.option("--date", "-d", help="New date (YYYY-MM-DD)")
@click.option("--desc", help="New description")
@handle_errors
def edit(expense_id, amount, category, date, desc):
    """Edit an existing expense."""
    with ExpenseService() as exp_service, CategoryService() as cat_service:
        if not exp_service.get_expense(expense_id):
            return fail(f"Expense #{expense_id} not found.")

        updates = {}
        if amount:
            value = parse_or_fail(validate_amount, amount)
            if value is None:
                return
            updates["amount"] = value

        if category:
            cat = resolve_category(cat_service, category)
            if not cat:
                return fail(f"Category '{category}' not found.")
            updates["category_id"] = cat.id

        if date:
            value = parse_or_fail(validate_date, date)
            if value is None:
                return
            updates["date"] = value

        if desc is not None:
            updates["description"] = desc

        if not updates:
            click.echo("No changes specified.")
            return

        if exp_service.update_expense(expense_id, **updates):
            click.echo(f"Expense #{expense_id} updated successfully.")
        else:
            click.echo("No changes made.")


@cli.command()
@click.argument("expense_id", type=int)
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
@handle_errors
def delete(expense_id, yes):
    """Delete an expense."""
    with ExpenseService() as exp_service:
        existing = exp_service.get_expense(expense_id)
        if not existing:
            return fail(f"Expense #{expense_id} not found.")

        if not yes:
            click.echo(f"Expense #{expense_id}: {format_date(existing.date)} - "
                       f"{existing.category_name} - {format_currency(existing.amount)}")
            if not click.confirm("Are you sure you want to delete this expense?"):
                click.echo("Delete cancelled.")
                return

        if exp_service.delete_expense(expense_id):
            click.echo(f"Expense #{expense_id} deleted successfully.")
        else:
            click.echo("Failed to delete expense.")


@cli.command()
@click.option("--month", "-m", default=datetime.now().strftime("%Y-%m"), help="Month (YYYY-MM)")
@handle_errors
def summary(month):
    """Show monthly expense summary."""
    with ExpenseService() as exp_service:
        validated_month = parse_or_fail(validate_month, month)
        if validated_month is None:
            return

        data = exp_service.get_monthly_summary(validated_month)

        if data["total"] == 0:
            click.echo(f"No expenses found for {validated_month}.")
            return

        click.echo(f"\nExpense Summary for {data['month']}")
        click.echo("=" * 40)

        rows = [[cat_name, format_currency(amount)]
                for cat_name, amount in data.items()
                if cat_name not in ("total", "month")]

        click.echo(format_table(["Category", "Amount"], rows))
        click.echo(f"\nTotal: {format_currency(data['total'])}")


@cli.group()
def category():
    """Manage expense categories."""
    pass


@category.command("list")
@handle_errors
def category_list():
    """List all categories."""
    with CategoryService() as cat_service:
        categories = cat_service.list_categories()

        if not categories:
            click.echo("No categories found.")
            return

        click.echo(format_table(["ID", "Name"], [[cat.id, cat.name] for cat in categories]))


@category.command("add")
@click.option("--name", "-n", required=True, help="Category name")
@handle_errors
def category_add(name):
    """Add a new category."""
    with CategoryService() as cat_service:
        cat_id = cat_service.add_category(name)
        click.echo(f"Category '{name}' added successfully (ID: {cat_id}).")


@category.command("delete")
@click.argument("category_id", type=int)
@handle_errors
def category_delete(category_id):
    """Delete a category."""
    with CategoryService() as cat_service:
        existing = cat_service.get_category(category_id)
        if not existing:
            return fail(f"Category #{category_id} not found.")

        if click.confirm(f"Delete category '{existing.name}'?"):
            if cat_service.delete_category(category_id):
                click.echo(f"Category '{existing.name}' deleted successfully.")
            else:
                click.echo("Failed to delete category.")


if __name__ == "__main__":
    cli()