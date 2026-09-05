import sqlite3
import unittest

from database import (
    add_transaction,
    create_table,
    get_balance,
    get_expense_report,
    get_transactions,
)
from validators import validate_date, validate_transaction


class TransactionValidationTests(unittest.TestCase):
    def test_accepts_valid_transaction_and_strips_text(self):
        self.assertEqual(
            validate_transaction("income", 1000, " Salary ", " August pay "),
            ("Salary", "August pay"),
        )

    def test_rejects_invalid_transaction_type(self):
        with self.assertRaises(ValueError):
            validate_transaction("transfer", 100, "Other", "")

    def test_rejects_non_positive_amount(self):
        with self.assertRaises(ValueError):
            validate_transaction("expense", 0, "Food", "")

    def test_validates_iso_dates(self):
        self.assertEqual(validate_date("2026-09-05"), "2026-09-05")
        with self.assertRaises(ValueError):
            validate_date("05.09.2026")


class DatabaseReportTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        create_table(self.conn)
        add_transaction(self.conn, "income", 100000, "Salary", "", "2026-09-01")
        add_transaction(self.conn, "expense", 12300, "Food", "", "2026-09-02")
        add_transaction(self.conn, "expense", 10000, "Housing", "", "2026-09-03")
        add_transaction(self.conn, "expense", 4200, "Transport", "", "2026-09-04")
        add_transaction(self.conn, "expense", 500, "Food", "", "2026-08-30")

    def tearDown(self):
        self.conn.close()

    def test_creates_and_reads_transactions(self):
        transactions = get_transactions(self.conn)
        self.assertEqual(len(transactions), 5)
        self.assertEqual(transactions[0][3], "Transport")

    def test_filters_by_period_and_category(self):
        transactions = get_transactions(
            self.conn, "2026-09-01", "2026-09-30", "food"
        )
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0][2], 12300)

    def test_calculates_monthly_balance(self):
        income, expenses = get_balance(self.conn, "2026-09")
        self.assertEqual((income, expenses), (100000, 26500))
        self.assertEqual(income - expenses, 73500)

    def test_returns_top_three_expense_categories(self):
        report = get_expense_report(self.conn, "2026-09")
        self.assertEqual(report, [("Food", 12300), ("Housing", 10000), ("Transport", 4200)])


if __name__ == "__main__":
    unittest.main()
