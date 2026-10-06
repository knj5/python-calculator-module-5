from app.operations import OperationFactory
from app.history import HistoryManager
from app.calculator_memento import CalculatorMemento, CalculatorCaretaker


class CalculatorObserver:
    """Observer interface for calculator events."""

    def update(self, operation, a, b, result):
        pass


class HistoryObserver(CalculatorObserver):
    """Observer that records completed calculations."""

    def __init__(self, history_manager):
        self.history_manager = history_manager

    def update(self, operation, a, b, result):
        self.history_manager.add(operation, a, b, result)


class Calculator:
    """Facade for calculator operations, history, and state management."""

    def __init__(self, config=None):
        self.config = config
        self.history = HistoryManager()
        self.caretaker = CalculatorCaretaker()
        self.observers = []
        self.last_result = None

        self.attach(HistoryObserver(self.history))

        if self.config is not None:
            history_path = self.config.history_path
            if history_path.exists():
                try:
                    self.history.load(history_path)
                except (OSError, ValueError):
                    pass

    def attach(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, operation, a, b, result):
        for observer in self.observers:
            observer.update(operation, a, b, result)

    def calculate(self, operation, a, b):
        """Execute an operation through the Strategy/Factory layer."""
        strategy = OperationFactory.create_operation(operation)

        if self.last_result is not None:
            self.caretaker.save(
                CalculatorMemento(self.last_result)
            )

        result = strategy.execute(a, b)
        self.last_result = result

        self.notify(operation, a, b, result)

        if (
            self.config is not None
            and self.config.auto_save
        ):
            self.save_history()

        return result

    def undo(self):
        memento = self.caretaker.undo()

        if memento is None:
            return None

        current = self.last_result

        if current is not None:
            self.caretaker._redo_stack[-1] = CalculatorMemento(current)

        self.last_result = memento.get_state()
        return self.last_result

    def redo(self):
        memento = self.caretaker.redo()

        if memento is None:
            return None

        self.last_result = memento.get_state()
        return self.last_result

    def clear_history(self):
        self.history.clear()

    def get_history(self):
        return self.history.get_history()

    def save_history(self, filename=None):
        if filename is None:
            if self.config is None:
                filename = "data/calculation_history.csv"
            else:
                filename = self.config.history_file

        self.history.save(filename)

    def load_history(self, filename=None):
        if filename is None:
            if self.config is None:
                filename = "data/calculation_history.csv"
            else:
                filename = self.config.history_file

        return self.history.load(filename)