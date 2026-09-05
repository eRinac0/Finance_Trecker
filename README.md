# Finance Tracker

Finance Tracker is a small command-line application for recording personal income and expenses. It stores transactions in SQLite, filters them by date or category, produces monthly summaries, and exports selected records to CSV.

## Technologies

- Python 3.10+
- SQLite (`sqlite3` from the standard library)
- `argparse` for the command-line interface
- `unittest` for automated tests

## Installation and launch

Clone the repository, then run the application from its folder:

```powershell
py main.py --help
```

No third-party packages are required. The SQLite database (`finance_tracker.db`) is created automatically on first launch.

## Commands

| Command | Description |
| --- | --- |
| `add --type income\|expense --amount AMOUNT --category CATEGORY [--description TEXT] [--date YYYY-MM-DD]` | Add a transaction. The date defaults to today. |
| `list [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--category NAME] [--export FILE.csv]` | List transactions for a period or category and optionally save exactly those results as CSV. |
| `delete` | Choose and remove a transaction by its ID. |
| `balance [--month YYYY-MM]` | Show income, expenses, and balance for all time or for one month. |
| `report --month YYYY-MM` | Show a monthly report and the top three expense categories. |

Run the test suite with:

```powershell
py -m unittest discover -s tests -v
```

## Examples

Add an income and an expense with explicit dates:

```powershell
py main.py add --type income --amount 100000 --category Salary --description "September salary" --date 2026-09-01
py main.py add --type expense --amount 12300 --category Food --description "Groceries" --date 2026-09-02
```

Filter a category within a date range and export the displayed records:

```powershell
py main.py list --from 2026-09-01 --to 2026-09-30 --category Food --export food-september.csv
```

Monthly report output:

```text
Report for 2026-09
Income: 100 000.00 RUB
Expenses: 32 400.00 RUB
Balance: 67 600.00 RUB

Top expense categories:
1. Food — 12 300.00 RUB
2. Housing — 10 000.00 RUB
3. Transport — 4 200.00 RUB
```

![Terminal report example](docs/terminal-demo.svg)

## Future ideas

- Configurable currency and locale-aware formatting
- Edit existing transactions
- Budget limits and notifications by category
- Charts and a simple web interface
