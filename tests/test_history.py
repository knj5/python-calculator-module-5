import pandas as pd
import pytest

from app.history import HistoryManager as History


def test_history_starts_empty():
    history = History()

    assert len(history) == 0
    assert history.get_history().empty


def test_add_history():
    history = History()
    history.add("add", 10, 5, 15)

    assert len(history) == 1

    data = history.get_history()
    assert data.iloc[0]["operation"] == "add"
    assert data.iloc[0]["a"] == 10
    assert data.iloc[0]["b"] == 5
    assert data.iloc[0]["result"] == 15


@pytest.mark.parametrize(
    "operation,a,b,result",
    [
        ("add", 10, 5, 15),
        ("subtract", 10, 5, 5),
        ("multiply", 10, 5, 50),
        ("divide", 10, 5, 2),
        ("power", 2, 3, 8),
        ("root", 9, 2, 3),
    ],
)
def test_add_multiple_operation_types(operation, a, b, result):
    history = History()
    history.add(operation, a, b, result)

    data = history.get_history()

    assert len(history) == 1
    assert data.iloc[0]["operation"] == operation
    assert data.iloc[0]["result"] == result


def test_clear_history():
    history = History()
    history.add("add", 1, 2, 3)
    history.add("multiply", 2, 4, 8)

    assert len(history) == 2

    history.clear()

    assert len(history) == 0
    assert history.get_history().empty


def test_get_history_returns_copy():
    history = History()
    history.add("add", 1, 2, 3)

    copied_history = history.get_history()
    copied_history.loc[0, "result"] = 999

    assert history.get_history().iloc[0]["result"] == 3


def test_save_and_load(tmp_path):
    filename = tmp_path / "history.csv"

    history = History()
    history.add("add", 10, 5, 15)
    history.add("power", 2, 3, 8)
    history.save(filename)

    assert filename.exists()

    loaded = History()
    result = loaded.load(filename)

    assert len(loaded) == 2
    pd.testing.assert_frame_equal(
        result.reset_index(drop=True),
        history.get_history().reset_index(drop=True),
        check_dtype=False,
    )


def test_save_creates_parent_directory(tmp_path):
    filename = tmp_path / "nested" / "folder" / "history.csv"

    history = History()
    history.add("add", 1, 1, 2)
    history.save(filename)

    assert filename.exists()


def test_load_missing_file(tmp_path):
    filename = tmp_path / "does_not_exist.csv"

    history = History()

    with pytest.raises(FileNotFoundError):
        history.load(filename)
