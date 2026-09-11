# Business Requirements Document (BRD)
## Personal Expense Tracker CLI Application

---

## 1. Executive Summary

A command-line interface (CLI) application for tracking personal expenses, built with Python using Click and SQLite. The application helps users log, categorize, and review their daily expenses with monthly summaries.

---

## 2. Project Overview

| Item | Details |
|------|---------|
| **Project Name** | Personal Expense Tracker |
| **Version** | 1.0.0 |
| **Platform** | CLI (Command-Line Interface) |
| **Language** | Python 3.7+ |
| **CLI Framework** | Click |
| **Database** | SQLite (local file-based) |
| **Authentication** | None (single-user) |

---

## 3. Functional Requirements

### 3.1 Expense Management
- Add new expense with amount, category, date, and description
- Edit existing expense entry
- Delete expense entry with confirmation
- List all expenses with optional filters

### 3.2 Category Management
- Predefined categories (Food, Transport, Entertainment, Utilities, Shopping, Health, Education, Other)
- Add custom categories
- List available categories
- Delete categories

### 3.3 Reporting & Summary
- Monthly expense summary (total by category)
- Filter expenses by month
- Filter expenses by category

---

## 4. Technical Architecture

### 4.1 Project Structure

```
expense-tracker/
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── expense_tracker/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point (Click commands)
│   ├── config.py           # Configuration constants
│   ├── database.py         # SQLite connection & setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── expense.py      # Expense dataclass
│   │   └── category.py     # Category dataclass
│   ├── services/
│   │   ├── __init__.py
│   │   ├── expense_service.py    # Expense CRUD operations
│   │   └── category_service.py   # Category operations
│   └── utils/
│       ├── __init__.py
│       ├── formatters.py   # Date/currency formatting
│       └── validators.py   # Input validation
├── tests/
│   └── __init__.py
└── data/
    └── expenses.db         # SQLite database (auto-created)
```

### 4.2 Database Schema

```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category_id INTEGER,
    date TEXT NOT NULL,
    description TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

---

## 5. CLI Commands Reference

### 5.1 Main Commands

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

### 5.2 Command Options

#### Add Expense
```bash
expense add --amount 50.00 --category Food --date 2026-09-11 --desc "Lunch"
expense add -a 25.50 -c Transport -d 2026-09-10 --desc "Bus fare"
```

#### List Expenses
```bash
expense list                         # List all expenses
expense list --month 2026-09         # Filter by month
expense list --category Food         # Filter by category
expense list -m 2026-09 -c Shopping  # Combined filters
```

#### Edit Expense
```bash
expense edit 1 --amount 45.00
expense edit 1 --category Entertainment
expense edit 1 -a 100 -c Shopping -d 2026-09-12 --desc "New item"
```

#### Delete Expense
```bash
expense delete 1         # With confirmation prompt
expense delete 1 --yes   # Skip confirmation
```

#### Monthly Summary
```bash
expense summary                    # Current month
expense summary --month 2026-09    # Specific month
```

#### Category Management
```bash
expense category list
expense category add --name "Gym"
expense category delete 1
```

---

## 6. User Stories

### Epic 1: Expense Management

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-001 | As a user, I want to add an expense so I can track my spending | Command accepts amount, category, date, description. Expense is saved to DB |
| US-002 | As a user, I want to edit an expense to correct mistakes | Can modify amount, category, date, or description of existing expense |
| US-003 | As a user, I want to delete an expense I no longer need | Expense is removed after confirmation |
| US-004 | As a user, I want to list all my expenses | Shows table with date, amount, category, description |

### Epic 2: Categories

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-005 | As a user, I want predefined expense categories | 8 default categories exist on first run |
| US-006 | As a user, I want to add custom categories | New category is available for future expenses |

### Epic 3: Reporting

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-007 | As a user, I want to see my monthly expense summary | Shows total spent and breakdown by category for given month |
| US-008 | As a user, I want to filter expenses by date range | Only expenses within specified month are shown |
| US-009 | As a user, I want to filter expenses by category | Only expenses in selected category are shown |

---

## 7. Dependencies

```
click>=8.0.0        # CLI framework
tabulate>=0.9.0     # Table formatting
```

---

## 8. Installation & Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .

# Run the application
expense --help
expense add --amount 50 --category Food
expense list
expense summary
```

---

## 9. Out of Scope (Future Enhancements)

- Budget limits and alerts
- Export to CSV/Excel
- Recurring expenses
- Multi-currency support
- Charts/visualizations
- Data backup/restore

---

## 10. Assumptions

- User has Python 3.7+ installed
- Single-user application (no multi-user support)
- Data stored locally only (no cloud sync)
- English language interface

---

**Document Version:** 1.0.0  
**Last Updated:** September 11, 2026
