class CalculatorError(Exception):
    """Base exception for calculator errors."""


class InvalidInputError(CalculatorError):
    """Raised when user input is invalid."""


class InvalidOperationError(CalculatorError):
    """Raised when an unsupported operation is requested."""


class CalculationError(CalculatorError):
    """Raised when a calculation cannot be completed."""


class ConfigurationError(CalculatorError):
    """Raised when configuration is invalid."""