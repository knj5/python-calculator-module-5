import pytest

from app.exceptions import (
    CalculatorError,
    InvalidInputError,
    InvalidOperationError,
    CalculationError,
    ConfigurationError,
)


@pytest.mark.parametrize(
    "exception_class",
    [
        CalculatorError,
        InvalidInputError,
        InvalidOperationError,
        CalculationError,
        ConfigurationError,
    ],
)
def test_exception_message(exception_class):
    message = "Test error message"
    error = exception_class(message)

    assert str(error) == message


@pytest.mark.parametrize(
    "exception_class",
    [
        InvalidInputError,
        InvalidOperationError,
        CalculationError,
        ConfigurationError,
    ],
)
def test_custom_exceptions_inherit_from_calculator_error(exception_class):
    error = exception_class("test")

    assert isinstance(error, CalculatorError)
    assert isinstance(error, Exception)


@pytest.mark.parametrize(
    "exception_class",
    [
        CalculatorError,
        InvalidInputError,
        InvalidOperationError,
        CalculationError,
        ConfigurationError,
    ],
)
def test_exceptions_can_be_raised(exception_class):
    with pytest.raises(exception_class):
        raise exception_class("expected error")
