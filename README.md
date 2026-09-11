# Personal Expense Tracker

A command-line interface (CLI) application for tracking personal expenses.

## Features

- Add, edit, delete expenses
- Predefined and custom categories
- Monthly expense summaries
- Filter by month and category
- Beautiful table output

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

```bash
# Add an expense
expense add --amount 50.00 --category Food --date 2026-09-11 --desc "Lunch"

# List all expenses
expense list

# List expenses by month
expense list --month 2026-09

# List expenses by category
expense list --category Food

# Edit an expense
expense edit 1 --amount 45.00

# Delete an expense
expense delete 1

# Monthly summary
expense summary

# Category management
expense category list
expense category add --name "Gym"
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `expense add` | Add a new expense |
| `expense list` | List expenses with filters |
| `expense edit <id>` | Edit an expense |
| `expense delete <id>` | Delete an expense |
| `expense summary` | Show monthly summary |
| `expense category list` | List all categories |
| `expense category add` | Add a new category |
| `expense category delete` | Delete a category |

## Logging

Logs are written to `data/logs/expense-tracker.log` (rotating, keeps 3 × 1MB backups). INFO+ messages also appear on stderr; the log file captures DEBUG detail and full tracebacks for unexpected errors.

## License

MIT
