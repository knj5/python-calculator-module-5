import pytest

from app.input_validators import validate_operation
from app.exceptions import InvalidInputError


@pytest.mark.parametrize(
    "operation,expected",
    [
        ("add", "add"),
        ("subtract", "subtract"),
        ("multiply", "multiply"),
        ("divide", "divide"),
        ("power", "power"),
        ("root", "root"),
        ("ADD", "add"),
        ("  multiply  ", "multiply"),
        ("PoWeR", "power"),
    ],
)
def test_validate_operation_valid(operation, expected):
    assert validate_operation(operation) == expected


@pytest.mark.parametrize(
    "operation",
    [
        "invalid",
        "",
        "modulo",
        "addition",
    ],
)
def test_validate_operation_invalid(operation):
    with pytest.raises(InvalidInputError):
        validate_operation(operation)


@pytest.mark.parametrize(
    "operation",
    [
        123,
        None,
        3.14,
        [],
    ],
)
def test_validate_operation_non_string(operation):
    with pytest.raises(InvalidInputError):
        validate_operation(operation)