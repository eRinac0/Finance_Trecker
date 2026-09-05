from datetime import date


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


def validate_date(value, allow_month=False):
    """Validate an ISO date or (when requested) a YYYY-MM month."""
    if value is None:
        return None

    expected_format = "%Y-%m" if allow_month else "%Y-%m-%d"
    try:
        parsed = date.fromisoformat(f"{value}-01" if allow_month else value)
    except ValueError as error:
        label = "month" if allow_month else "date"
        raise ValueError(f"{label.capitalize()} must use {expected_format} format.") from error

    return parsed.strftime(expected_format)
