from app.calculator_memento import CalculatorMemento, CalculatorCaretaker


def test_memento_state():
    state = {"result": 10}
    memento = CalculatorMemento(state)

    assert memento.get_state() == state


def test_caretaker_counts():
    caretaker = CalculatorCaretaker()

    assert caretaker.undo_count == 0
    assert caretaker.redo_count == 0