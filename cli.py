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

    subparsers.add_parser(
        "list",
        help="List all transactions"
    )

    subparsers.add_parser(
        "delete",
        help="Delete a transaction"
    )

    subparsers.add_parser(
        "balance",
        help="Calculate total balance"
    )

    subparsers.add_parser(
        "report",
         help="Generate monthly report"
    )

   
    return parser.parse_args()