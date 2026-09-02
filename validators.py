def validate_transaction(transaction_type, amount, category, description):
    if transaction_type not in ("income", "expense"):
        raise ValueError(
            "Transaction type must be 'income' or 'expense'."
        )

    if amount <= 0:
        raise ValueError(
            "Amount must be greater than zero."
        )

    category = category.strip()

    if not category:
        raise ValueError(
            "Category cannot be empty."
        )

    description = description.strip()

    return category, description