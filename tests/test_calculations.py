import pytest

from app.calculator import Calculator


@pytest.fixture
def calculator():
    return Calculator()


def test_calculator_addition(calculator):
    result = calculator.calculate("add", 2, 3)
    assert result == 5


def test_calculator_subtraction(calculator):
    result = calculator.calculate("subtract", 10, 4)
    assert result == 6


def test_calculator_multiplication(calculator):
    result = calculator.calculate("multiply", 3, 4)
    assert result == 12


def test_calculator_division(calculator):
    result = calculator.calculate("divide", 10, 2)
    assert result == 5


def test_calculator_power(calculator):
    result = calculator.calculate("power", 2, 3)
    assert result == 8


def test_calculator_root(calculator):
    result = calculator.calculate("root", 9, 2)
    assert result == 3


def test_last_result(calculator):
    calculator.calculate("add", 5, 5)
    assert calculator.last_result == 10


def test_clear_history(calculator):
    calculator.calculate("add", 2, 3)

    assert len(calculator.get_history()) > 0

    calculator.clear_history()

    assert len(calculator.get_history()) == 0


def test_get_history(calculator):
    calculator.calculate("add", 2, 3)

    history = calculator.get_history()

    assert history is not None
    assert len(history) == 1


def test_calculator_without_config():
    calculator = Calculator()

    assert calculator.config is None


def test_attach_and_detach_observer(calculator):
    class TestObserver:
        def update(self, operation, a, b, result):
            pass

    observer = TestObserver()

    calculator.attach(observer)

    assert observer in calculator.observers

    calculator.detach(observer)

    assert observer not in calculator.observers


def test_observer_is_not_duplicated(calculator):
    class TestObserver:
        def update(self, operation, a, b, result):
            pass

    observer = TestObserver()

    calculator.attach(observer)
    calculator.attach(observer)

    assert calculator.observers.count(observer) == 1


def test_notify_observer(calculator):
    received = {}

    class TestObserver:
        def update(self, operation, a, b, result):
            received["operation"] = operation
            received["a"] = a
            received["b"] = b
            received["result"] = result

    observer = TestObserver()

    calculator.attach(observer)

    calculator.calculate("add", 2, 3)

    assert received["operation"] == "add"
    assert received["a"] == 2
    assert received["b"] == 3
    assert received["result"] == 5


def test_save_history(monkeypatch):
    calculator = Calculator()

    saved = {}

    def fake_save(filename):
        saved["filename"] = filename

    monkeypatch.setattr(
        calculator.history,
        "save",
        fake_save
    )

    calculator.save_history("test_history.csv")

    assert saved["filename"] == "test_history.csv"


def test_load_history(monkeypatch):
    calculator = Calculator()

    loaded = {}

    def fake_load(filename):
        loaded["filename"] = filename
        return None

    monkeypatch.setattr(
        calculator.history,
        "load",
        fake_load
    )

    calculator.load_history("test_history.csv")

    assert loaded["filename"] == "test_history.csv"


def test_default_save_and_load_history(monkeypatch):
    calculator = Calculator()

    saved = {}
    loaded = {}

    def fake_save(filename):
        saved["filename"] = filename

    def fake_load(filename):
        loaded["filename"] = filename
        return None

    monkeypatch.setattr(
        calculator.history,
        "save",
        fake_save
    )

    monkeypatch.setattr(
        calculator.history,
        "load",
        fake_load
    )

    calculator.save_history()
    calculator.load_history()

    assert saved["filename"] == "data/calculation_history.csv"
    assert loaded["filename"] == "data/calculation_history.csv"

def test_calculator_bad_existing_history(monkeypatch, tmp_path):
    from app.calculator_config import CalculatorConfig
    from app.history import HistoryManager

    history_file = tmp_path / "history.csv"
    history_file.touch()

    config = CalculatorConfig()
    config.history_file = str(history_file)

    def fake_load(self, filename):
        raise ValueError("bad history")

    monkeypatch.setattr(HistoryManager, "load", fake_load)

    calculator = Calculator(config)

    assert calculator is not None

def test_base_calculator_observer_update():
    from app.calculator import CalculatorObserver

    observer = CalculatorObserver()

    result = observer.update("add", 2, 3, 5)

    assert result is None