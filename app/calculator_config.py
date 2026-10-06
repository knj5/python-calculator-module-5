import os
from pathlib import Path
from dotenv import load_dotenv


class CalculatorConfig:
    """Manages calculator configuration using environment variables."""

    def __init__(self):
        load_dotenv()

        self.history_file = os.getenv(
            "HISTORY_FILE",
            "data/calculation_history.csv"
        )

        self.max_history = self._get_positive_int(
            "MAX_HISTORY",
            100
        )

        self.auto_save = self._get_bool(
            "AUTO_SAVE",
            True
        )

    @staticmethod
    def _get_positive_int(name, default):
        value = os.getenv(name)

        if value is None:
            return default

        try:
            value = int(value)
        except ValueError as exc:
            raise ValueError(
                f"{name} must be an integer."
            ) from exc

        if value <= 0:
            raise ValueError(
                f"{name} must be greater than zero."
            )

        return value

    @staticmethod
    def _get_bool(name, default):
        value = os.getenv(name)

        if value is None:
            return default

        normalized = value.strip().lower()

        if normalized in {"true", "1", "yes", "on"}:
            return True

        if normalized in {"false", "0", "no", "off"}:
            return False

        raise ValueError(
            f"{name} must be a valid boolean value."
        )

    @property
    def history_path(self):
        return Path(self.history_file)