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
expense --help
```

## Example Prompts

Try these prompts to get started with the expense tracker:

1. **Add a new expense**
   ```bash
   expense add --amount 50.00 --category Food --date 2026-09-11 --desc "Lunch"
   ```

2. **List all expenses**
   ```bash
   expense list
   ```

3. **Filter expenses by month**
   ```bash
   expense list --month 2026-09
   ```

4. **Filter expenses by category**
   ```bash
   expense list --category Food
   ```

5. **View the monthly expense summary**
   ```bash
   expense summary
   ```

6. **Edit an existing expense**
   ```bash
   expense edit 1 --amount 45.00
   ```

7. **Delete an expense**
   ```bash
   expense delete 1
   ```

8. **Manage categories**
   ```bash
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
