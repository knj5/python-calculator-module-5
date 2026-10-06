from pathlib import Path
import pandas as pd


class HistoryManager:
    """Stores and persists calculator history using a pandas DataFrame."""

    COLUMNS = ["operation", "a", "b", "result"]

    def __init__(self):
        self.history = pd.DataFrame(columns=self.COLUMNS)

    def add(self, operation, a, b, result):
        new_entry = pd.DataFrame(
            [{
                "operation": operation,
                "a": a,
                "b": b,
                "result": result,
            }]
        )
        self.history = pd.concat(
            [self.history, new_entry],
            ignore_index=True
        )

    def clear(self):
        self.history = pd.DataFrame(columns=self.COLUMNS)

    def get_history(self):
        return self.history.copy()

    def save(self, filename):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.history.to_csv(path, index=False)

    def load(self, filename):
        path = Path(filename)

        if not path.exists():
            raise FileNotFoundError(f"History file not found: {filename}")

        self.history = pd.read_csv(path)
        return self.history

    def __len__(self):
        return len(self.history)