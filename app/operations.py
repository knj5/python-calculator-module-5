from abc import ABC, abstractmethod
import math


class Operation(ABC):
    """Abstract strategy for calculator operations."""

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass


class Addition(Operation):
    def execute(self, a, b):
        return a + b


class Subtraction(Operation):
    def execute(self, a, b):
        return a - b


class Multiplication(Operation):
    def execute(self, a, b):
        return a * b


class Division(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b


class Power(Operation):
    def execute(self, a, b):
        return a ** b


class Root(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ValueError("Root degree cannot be zero.")
        if a < 0 and int(b) % 2 == 0:
            raise ValueError("Cannot take an even root of a negative number.")
        if a < 0:
            return -((-a) ** (1 / b))
        return a ** (1 / b)


class OperationFactory:
    """Factory for creating operation strategies."""

    operations = {
        "add": Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
        "power": Power,
        "root": Root,
    }

    @classmethod
    def create_operation(cls, operation_name: str) -> Operation:
        operation = cls.operations.get(operation_name.lower())

        if operation is None:
            raise ValueError(f"Unknown operation: {operation_name}")

        return operation()