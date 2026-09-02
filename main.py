import sqlite3


def main():
    print("Welcome to the Finance Tracker!")
    main_choice ={
        "1": "Add transaction",
        "2": "View all transactions",
        "3": "Calculate total balance",
        "0": "Exit"
    }
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
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
    while True:
        print("\nPlease choose an option:")
        for key, value in main_choice.items():
            print(f"{key}: {value}")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_transaction(conn, cursor)
        elif choice == "2":
            view_transactions(conn, cursor)
        elif choice == "3":
            calculate_balance(conn, cursor)
        elif choice == "0":
            print("Exiting the Finance Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def add_transaction(conn, cursor):
    type = input("Enter transaction type (income/expense): ").split()[0].lower()
    amount = float(input("Enter transaction amount: "))
    category = input("Enter transaction category: ")
    description = input("Enter transaction description: ")
    date = input("Enter transaction date (YYYY-MM-DD): ")
    cursor.execute("""
        INSERT INTO transactions (type, amount, category, description, date)
        VALUES (?, ?, ?, ?, ?)
    """, (type, amount, category, description, date))
    conn.commit()
    print("Transaction added successfully!")

def view_transactions(conn, cursor):
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    if not transactions:
        print("No transactions found.")
        return
    print("\nAll Transactions:")
    for i, transaction in enumerate(transactions, start=1):
        print(f"{i}. {transaction[5]} - {transaction[1].capitalize()} - {transaction[4]} - ${transaction[2]:.2f} - {transaction[3]}")

def calculate_balance(conn, cursor):
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
    total_income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
    total_expense = cursor.fetchone()[0] or 0
    balance = total_income - total_expense
    print(f"\nTotal Income: ${total_income:.2f}")
    print(f"Total Expense: ${total_expense:.2f}")
    print(f"Total Balance: ${balance:.2f}")
    


main()

