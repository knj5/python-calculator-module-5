import pytest
from pathlib import Path

from app.calculator_config import CalculatorConfig


def clear_config_env(monkeypatch):
    monkeypatch.delenv("HISTORY_FILE", raising=False)
    monkeypatch.delenv("MAX_HISTORY", raising=False)
    monkeypatch.delenv("AUTO_SAVE", raising=False)


def test_config_defaults(monkeypatch):
    clear_config_env(monkeypatch)

    config = CalculatorConfig()

    assert config.history_file == "data/calculation_history.csv"
    assert config.max_history == 100
    assert config.auto_save is True
    assert config.history_path == Path("data/calculation_history.csv")


def test_config_custom_values(monkeypatch):
    monkeypatch.setenv("HISTORY_FILE", "custom/history.csv")
    monkeypatch.setenv("MAX_HISTORY", "50")
    monkeypatch.setenv("AUTO_SAVE", "false")

    config = CalculatorConfig()

    assert config.history_file == "custom/history.csv"
    assert config.max_history == 50
    assert config.auto_save is False
    assert config.history_path == Path("custom/history.csv")


@pytest.mark.parametrize("value", ["true", "1", "yes", "on", " TRUE ", "YES"])
def test_auto_save_true_values(monkeypatch, value):
    clear_config_env(monkeypatch)
    monkeypatch.setenv("AUTO_SAVE", value)

    config = CalculatorConfig()

    assert config.auto_save is True


@pytest.mark.parametrize("value", ["false", "0", "no", "off", " FALSE ", "NO"])
def test_auto_save_false_values(monkeypatch, value):
    clear_config_env(monkeypatch)
    monkeypatch.setenv("AUTO_SAVE", value)

    config = CalculatorConfig()

    assert config.auto_save is False


@pytest.mark.parametrize("value", ["abc", "1.5", "", "ten"])
def test_max_history_must_be_integer(monkeypatch, value):
    clear_config_env(monkeypatch)
    monkeypatch.setenv("MAX_HISTORY", value)

    with pytest.raises(ValueError):
        CalculatorConfig()


@pytest.mark.parametrize("value", ["0", "-1", "-100"])
def test_max_history_must_be_positive(monkeypatch, value):
    clear_config_env(monkeypatch)
    monkeypatch.setenv("MAX_HISTORY", value)

    with pytest.raises(ValueError):
        CalculatorConfig()


@pytest.mark.parametrize("value", ["maybe", "invalid", "2", "truth"])
def test_auto_save_invalid_value(monkeypatch, value):
    clear_config_env(monkeypatch)
    monkeypatch.setenv("AUTO_SAVE", value)

    with pytest.raises(ValueError):
        CalculatorConfig()

def test_get_positive_int_default(monkeypatch):
    monkeypatch.delenv("TEST_INT", raising=False)
    assert CalculatorConfig._get_positive_int("TEST_INT", 42) == 42


def test_get_bool_default(monkeypatch):
    monkeypatch.delenv("TEST_BOOL", raising=False)
    assert CalculatorConfig._get_bool("TEST_BOOL", True) is True