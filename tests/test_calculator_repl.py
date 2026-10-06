from unittest.mock import patch

import pytest

from app.calculator_repl import run_calculator, main


def run_with_inputs(inputs):
    with patch("builtins.input", side_effect=inputs):
        run_calculator()


def test_exit(capsys):
    run_with_inputs(["exit"])
    output = capsys.readouterr().out
    assert "Professional Python Calculator" in output
    assert "Goodbye!" in output


def test_help(capsys):
    run_with_inputs(["help", "exit"])
    output = capsys.readouterr().out
    assert "Available commands:" in output


def test_history_empty(capsys):
    run_with_inputs(["clear", "history", "exit"])
    output = capsys.readouterr().out
    assert "No calculation history." in output


def test_calculation_and_history(capsys):
    run_with_inputs(["add", "2", "3", "history", "exit"])
    output = capsys.readouterr().out
    assert "Result: 5" in output
    assert "add" in output


def test_clear(capsys):
    run_with_inputs(["add", "2", "3", "clear", "history", "exit"])
    output = capsys.readouterr().out
    assert "History cleared." in output
    assert "No calculation history." in output


def test_undo_nothing(capsys):
    run_with_inputs(["undo", "exit"])
    output = capsys.readouterr().out
    assert "Nothing to undo." in output


def test_undo_and_redo(capsys):
    run_with_inputs(["add", "2", "3", "multiply", "4", "5",
                     "undo", "redo", "exit"])
    output = capsys.readouterr().out
    assert "Result: 5" in output
    assert "Result: 20" in output


def test_redo_nothing(capsys):
    run_with_inputs(["redo", "exit"])
    output = capsys.readouterr().out
    assert "Nothing to redo." in output


def test_save(capsys, tmp_path, monkeypatch):
    monkeypatch.setenv("HISTORY_FILE", str(tmp_path / "history.csv"))
    run_with_inputs(["add", "2", "3", "save", "exit"])
    output = capsys.readouterr().out
    assert "History saved." in output


def test_load_missing(capsys, tmp_path, monkeypatch):
    monkeypatch.setenv("HISTORY_FILE", str(tmp_path / "missing.csv"))
    run_with_inputs(["load", "exit"])
    output = capsys.readouterr().out
    assert "No saved history found." in output


def test_save_then_load(capsys, tmp_path, monkeypatch):
    history_file = tmp_path / "history.csv"
    monkeypatch.setenv("HISTORY_FILE", str(history_file))

    run_with_inputs(["add", "4", "6", "save", "exit"])
    run_with_inputs(["load", "history", "exit"])

    output = capsys.readouterr().out
    assert "History loaded." in output
    assert "add" in output


@pytest.mark.parametrize(
    "inputs",
    [
        ["divide", "10", "0", "exit"],
        ["invalid", "exit"],
        ["add", "abc", "2", "exit"],
    ],
)
def test_errors(inputs, capsys):
    run_with_inputs(inputs)
    output = capsys.readouterr().out
    assert "Error:" in output


def test_main():
    with patch("app.calculator_repl.run_calculator") as mocked_run:
        main()
        mocked_run.assert_called_once()


def test_repl_load_history_file_not_found(monkeypatch, capsys):
    from app.calculator_repl import run_calculator
    from app.calculator import Calculator

    commands = iter(["load", "exit"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(commands)
    )

    def fake_load_history(self, filename=None):
        raise FileNotFoundError

    monkeypatch.setattr(
        Calculator,
        "load_history",
        fake_load_history
    )

    run_calculator()

    captured = capsys.readouterr()

    assert "No saved history found." in captured.out

    def test_repl_load_history_file_not_found_continue(monkeypatch, capsys):
        from app.calculator_repl import run_calculator
        from app.calculator import Calculator

    commands = iter(["load", "exit"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(commands)
    )

    def fake_load_history(self, filename=None):
        raise FileNotFoundError

    monkeypatch.setattr(
        Calculator,
        "load_history",
        fake_load_history
    )

    run_calculator()

    output = capsys.readouterr().out
    assert "No saved history found." in output
def test_repl_load_history_file_not_found_continue(monkeypatch, capsys):
    from app.calculator_repl import run_calculator
    from app.calculator import Calculator

    commands = iter(["load", "exit"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(commands)
    )

    def fake_load_history(self, filename=None):
        raise FileNotFoundError

    monkeypatch.setattr(
        Calculator,
        "load_history",
        fake_load_history
    )

    run_calculator()

    output = capsys.readouterr().out
    assert "No saved history found." in output
