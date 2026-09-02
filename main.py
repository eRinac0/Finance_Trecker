def main():
    print("Welcome to the Finance Tracker!")
    main_choice ={
        "1": "Add transaction",
        "2": "View all transactions",
        "3": "Calculate total balance",
        "0": "Exit"
    }
    transactions = []
    while True:
        print("\nPlease choose an option:")
        for key, value in main_choice.items():
            print(f"{key}: {value}")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            calculate_balance(transactions)
        elif choice == "0":
            print("Exiting the Finance Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def add_transaction(transactions):
    type = input("Enter transaction type (income/expense): ").split()[0].lower()
    amount = float(input("Enter transaction amount: "))
    category = input("Enter transaction category: ")
    description = input("Enter transaction description: ")
    date = input("Enter transaction date (YYYY-MM-DD): ")
    transaction = {
        "type": type,
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }
    transactions.append(transaction)
    print("Transaction added successfully!")

def view_transactions(transactions):
    if not transactions:
        print("No transactions found.")
        return
    print("\nAll Transactions:")
    for i, transaction in enumerate(transactions, start=1):
        print(f"{i}. {transaction['date']} - {transaction['type'].capitalize()} - {transaction['category']} - ${transaction['amount']:.2f} - {transaction['description']}")

def calculate_balance(transactions):
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    balance = total_income - total_expense
    print(f"\nTotal Income: ${total_income:.2f}")
    print(f"Total Expense: ${total_expense:.2f}")
    print(f"Total Balance: ${balance:.2f}")
    


main()

