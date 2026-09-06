import csv
from validators import validate_date, validate_transaction
from cli import parse_arguments

from database import (
    create_connection,
    create_table,
    add_transaction,
    get_all_transactions,
    get_transactions,
    delete_transaction,
    get_balance,
    get_expense_report,
)


def format_money(amount):
    return f"{amount:,.2f}".replace(",", " ") + " EUR"


def export_transactions(transactions, file_name):
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Type", "Amount", "Category", "Description", "Date"])
        writer.writerows(transactions)


def print_transactions(transactions):
    if not transactions:
        print("No transactions found.")
        return

    print("\nAll transactions:")

    for transaction in transactions:
        transaction_id = transaction[0]
        transaction_type = transaction[1]
        amount = transaction[2]
        category = transaction[3]
        description = transaction[4]
        date = transaction[5]

        print(
            f"{transaction_id}. {date} | "
            f"{transaction_type.capitalize()} | "
            f"{category} | "
            f"{format_money(amount)} | "
            f"{description}"
        )


def main():
    args = parse_arguments()

    conn = create_connection()
    create_table(conn)

    try:
        if args.command == "add":
            try:
                category, description = validate_transaction(
                    args.type,
                    args.amount,
                    args.category,
                    args.description
                )
                transaction_date = validate_date(args.date)

            except ValueError as error:
                print(f"Validation error: {error}")
                return

            add_transaction(
                conn,
                args.type,
                args.amount,
                category,
                description,
                transaction_date
            )

            print("Transaction added successfully!")

        elif args.command == "list":
            try:
                date_from = validate_date(args.date_from)
                date_to = validate_date(args.date_to)
            except ValueError as error:
                print(f"Validation error: {error}")
                return
            transactions = get_transactions(
                conn, date_from, date_to, args.category
            )
            print_transactions(transactions)
            if args.export:
                export_transactions(transactions, args.export)
                print(f"Transactions exported to {args.export}")

        elif args.command == "delete":
            transactions = get_all_transactions(conn)
            print_transactions(transactions)

            if not transactions:
                return

            try:
                transaction_id = int(
                    input("Enter the ID of the transaction to delete: ")
                )

                if transaction_id <= 0:
                    print("ID must be a positive number.")
                    return
            except ValueError:
                print("ID must be a whole number, for example: 3.")
                return

            was_deleted = delete_transaction(conn, transaction_id)

            if was_deleted:
                print("Transaction deleted successfully!")
            else:
                print("Transaction with this ID was not found.")

        elif args.command == "balance":
            try:
                month = validate_date(args.month, allow_month=True)
            except ValueError as error:
                print(f"Validation error: {error}")
                return
            total_income, total_expense = get_balance(conn, month)
            balance = total_income - total_expense

            print(f"\nTotal income: {format_money(total_income)}")
            print(f"Total expenses: {format_money(total_expense)}")
            print(f"Total balance: {format_money(balance)}")

        elif args.command == "report":
            try:
                month = validate_date(args.month, allow_month=True)
            except ValueError as error:
                print(f"Validation error: {error}")
                return
            total_income, total_expense = get_balance(conn, month)
            balance = total_income - total_expense
            report = get_expense_report(conn, month)

            print(f"\nReport for {month}")
            print(f"Income: {format_money(total_income)}")
            print(f"Expenses: {format_money(total_expense)}")
            print(f"Balance: {format_money(balance)}")
            print("\nTop expense categories:")
            if not report:
                print("No expenses found for this period.")
            for index, (category, total) in enumerate(report, start=1):
                print(f"{index}. {category} — {format_money(total)}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
