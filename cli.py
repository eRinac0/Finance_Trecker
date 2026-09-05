import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Finance Tracker"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    add_parser = subparsers.add_parser(
        "add",
        help="Add a new transaction"
    )

    add_parser.add_argument(
        "--type",
        choices=["income", "expense"],
        required=True,
        help="Type of transaction"
    )
    add_parser.add_argument(
        "--amount",
        type=float,
        required=True,
        help="Amount of the transaction"
    )
    add_parser.add_argument(
        "--category",
        required=True,
        help="Category"
    )
    add_parser.add_argument(
        "--description",
        default="",
        help="Description"
    )
    add_parser.add_argument(
        "--date",
        help="Transaction date in YYYY-MM-DD format (default: today)"
    )

    list_parser = subparsers.add_parser(
        "list",
        help="List all transactions"
    )
    add_filter_arguments(list_parser)
    list_parser.add_argument(
        "--export",
        metavar="FILE",
        help="Save the listed transactions to a CSV file"
    )

    subparsers.add_parser(
        "delete",
        help="Delete a transaction"
    )

    balance_parser = subparsers.add_parser(
        "balance",
        help="Calculate total balance"
    )
    balance_parser.add_argument(
        "--month",
        help="Month in YYYY-MM format (default: all time)"
    )

    report_parser = subparsers.add_parser(
        "report",
        help="Generate monthly report"
    )
    report_parser.add_argument(
        "--month",
        required=True,
        help="Month in YYYY-MM format"
    )

    return parser.parse_args()


def add_filter_arguments(parser):
    """Add shared filters for commands that return transaction lists."""
    parser.add_argument(
        "--from",
        dest="date_from",
        metavar="YYYY-MM-DD",
        help="Include transactions from this date"
    )
    parser.add_argument(
        "--to",
        dest="date_to",
        metavar="YYYY-MM-DD",
        help="Include transactions through this date"
    )
    parser.add_argument(
        "--category",
        help="Filter by category (case-insensitive)"
    )
