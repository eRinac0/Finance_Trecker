import sqlite3
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parent
DB_NAME = PROJECT_FOLDER / "finance_tracker.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


def create_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            description TEXT,
            date DATE
        )
        """
    )
    conn.commit()


def add_transaction(
    conn, transaction_type, amount, category, description, transaction_date=None
):
    date_value = transaction_date or None
    conn.execute(
        """
        INSERT INTO transactions (type, amount, category, description, date)
        VALUES (?, ?, ?, ?, COALESCE(?, DATE('now')))
        """,
        (transaction_type, amount, category, description, date_value),
    )

    conn.commit()


def get_all_transactions(conn):
    return get_transactions(conn)


def get_transactions(conn, date_from=None, date_to=None, category=None):
    """Return transactions matching optional inclusive date and category filters."""
    conditions = []
    parameters = []

    if date_from:
        conditions.append("date >= ?")
        parameters.append(date_from)
    if date_to:
        conditions.append("date <= ?")
        parameters.append(date_to)
    if category:
        conditions.append("LOWER(category) = LOWER(?)")
        parameters.append(category.strip())

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    cursor = conn.execute(
        """
        SELECT * FROM transactions
        {where_clause}
        ORDER BY date DESC, id DESC
        """.format(where_clause=where_clause),
        parameters,
    )

    return cursor.fetchall()


def delete_transaction(conn, transaction_id):
    cursor = conn.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    conn.commit()

    return cursor.rowcount > 0


def get_balance(conn, month=None):
    """Return total income and expenses, optionally for a YYYY-MM month."""
    conditions = []
    parameters = []
    if month:
        conditions.append("strftime('%Y-%m', date) = ?")
        parameters.append(month)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    cursor = conn.execute(
        """
        SELECT
            COALESCE(SUM(CASE WHEN type = 'income' THEN amount END), 0),
            COALESCE(SUM(CASE WHEN type = 'expense' THEN amount END), 0)
        FROM transactions
        {where_clause}
        """.format(where_clause=where_clause),
        parameters,
    )
    return cursor.fetchone()


def get_expense_report(conn, month=None, limit=3):
    conditions = ["type = 'expense'"]
    parameters = []
    if month:
        conditions.append("strftime('%Y-%m', date) = ?")
        parameters.append(month)

    cursor = conn.execute(
        """
        SELECT category, SUM(amount)
        FROM transactions
        WHERE {conditions}
        GROUP BY category
        ORDER BY SUM(amount) DESC
        LIMIT ?
        """.format(conditions=" AND ".join(conditions)),
        parameters + [limit],
    )

    return cursor.fetchall()
