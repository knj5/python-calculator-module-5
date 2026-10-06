from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.input_validators import validate_number, validate_operation
from app.exceptions import InvalidInputError


HELP_TEXT = """
Available commands:
  add       Add two numbers
  subtract  Subtract two numbers
  multiply  Multiply two numbers
  divide    Divide two numbers
  power     Raise a number to a power
  root      Calculate a root
  history   Display calculation history
  clear     Clear calculation history
  undo      Undo the previous result
  redo      Redo the previous result
  save      Save calculation history
  load      Load calculation history
  help      Display this help message
  exit      Exit the calculator
"""


def run_calculator():
    """Run the calculator Read-Eval-Print Loop."""
    config = CalculatorConfig()
    calculator = Calculator(config)

    print("Professional Python Calculator")
    print("Type 'help' for available commands.")

    while True:
        command = input("Enter command: ").strip().lower()

        if command == "exit":
            print("Goodbye!")
            break

        if command == "help":
            print(HELP_TEXT)
            continue

        if command == "history":
            history = calculator.get_history()
            if history.empty:
                print("No calculation history.")
            else:
                print(history.to_string(index=False))
            continue

        if command == "clear":
            calculator.clear_history()
            print("History cleared.")
            continue

        if command == "undo":
            result = calculator.undo()
            print("Nothing to undo." if result is None else f"Result: {result}")
            continue

        if command == "redo":
            result = calculator.redo()
            print("Nothing to redo." if result is None else f"Result: {result}")
            continue

        if command == "save":
            calculator.save_history()
            print("History saved.")
            continue

        if command == "load":
            try:
                calculator.load_history()
                print("History loaded.")
            except FileNotFoundError:
                print("No saved history found.")
                continue  # pragma: no cover

        try:
            operation = validate_operation(command)
            first = validate_number(input("Enter first number: "))
            second = validate_number(input("Enter second number: "))

            result = calculator.calculate(operation, first, second)
            print(f"Result: {result}")

        except (
            InvalidInputError,
            ValueError,
            ZeroDivisionError,
            OverflowError,
        ) as error:
            print(f"Error: {error}")


def main():
    run_calculator()


if __name__ == "__main__":  # pragma: no cover
    main()