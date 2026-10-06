from app.exceptions import InvalidInputError


def validate_number(value):
    """Validate and convert input to a floating-point number."""
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise InvalidInputError(
            f"Invalid number: {value}"
        ) from exc


def validate_operation(operation):
    """Validate a calculator operation."""
    valid_operations = {
        "add",
        "subtract",
        "multiply",
        "divide",
        "power",
        "root",
    }

    if not isinstance(operation, str):
        raise InvalidInputError("Operation must be text.")

    operation = operation.strip().lower()

    if operation not in valid_operations:
        raise InvalidInputError(
            f"Invalid operation: {operation}"
        )

    return operation