import sqlite3
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parent
DB_NAME = PROJECT_FOLDER / "finance_tracker.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            description TEXT,
            date DATE
        )
    """)
    conn.commit()


def add_transaction(conn, transaction_type, amount, category, description):
    conn.execute("""
        INSERT INTO transactions (type, amount, category, description, date)
        VALUES (?, ?, ?, ?, DATE('now'))
    """, (transaction_type, amount, category, description))

    conn.commit()


def get_all_transactions(conn):
    cursor = conn.execute("""
        SELECT * FROM transactions
        ORDER BY date DESC, id DESC
    """)

    return cursor.fetchall()


def delete_transaction(conn, transaction_id):
    cursor = conn.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    conn.commit()

    return cursor.rowcount > 0


def get_balance(conn):
    income_cursor = conn.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type = 'income'
    """)
    total_income = income_cursor.fetchone()[0] or 0

    expense_cursor = conn.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type = 'expense'
    """)
    total_expense = expense_cursor.fetchone()[0] or 0

    return total_income, total_expense


def get_expense_report(conn):
    cursor = conn.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE type = 'expense'
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    return cursor.fetchall()