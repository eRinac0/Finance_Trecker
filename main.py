import csv
from validators import validate_transaction
from cli import parse_arguments

from database import (
    create_connection,
    create_table,
    add_transaction,
    get_all_transactions,
    delete_transaction,
    get_balance,
    get_expense_report,
)


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
            f"${amount:.2f} | "
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

            except ValueError as error:

                print(f"Validation error: {error}")
                return

            add_transaction(
                conn,
                args.type,
                args.amount,
                category,
                description
            )

            print("Transaction added successfully!")

        elif args.command == "list":
            transactions = get_all_transactions(conn)
            print_transactions(transactions)

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
            total_income, total_expense = get_balance(conn)
            balance = total_income - total_expense

            print(f"\nTotal income: ${total_income:.2f}")
            print(f"Total expense: ${total_expense:.2f}")
            print(f"Total balance: ${balance:.2f}")

        elif args.command == "report":
            report = get_expense_report(conn)

            if not report:
                print("No expense transactions found.")
                return

            print("\nTop-3 most expensive expenses by category:")

            for category, total in report:
                print(f"{category}: ${total:.2f}")

        elif args.command == "export":
            transactions = get_all_transactions(conn)

            if not transactions:
                print("No transactions found.")
                return

            with open(
                "transactions_export.csv",
                "w",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.writer(file)

                writer.writerow([
                    "ID",
                    "Type",
                    "Amount",
                    "Category",
                    "Description",
                    "Date",
                ])

                writer.writerows(transactions)

            print("Transactions exported to transactions_export.csv")

    finally:
        conn.close()


if __name__ == "__main__":
    main()