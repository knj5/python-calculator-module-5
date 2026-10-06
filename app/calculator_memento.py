from dataclasses import dataclass
from typing import Any


@dataclass
class CalculatorMemento:
    """Stores a snapshot of calculator state."""
    state: Any

    def get_state(self):
        return self.state


class CalculatorCaretaker:
    """Manages calculator snapshots for undo and redo."""

    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def save(self, memento: CalculatorMemento):
        self._undo_stack.append(memento)
        self._redo_stack.clear()

    def undo(self):
        if not self._undo_stack:
            return None
        memento = self._undo_stack.pop()
        self._redo_stack.append(memento)
        return memento

    def redo(self):
        if not self._redo_stack:
            return None
        memento = self._redo_stack.pop()
        self._undo_stack.append(memento)
        return memento

    @property
    def undo_count(self):
        return len(self._undo_stack)

    @property
    def redo_count(self):
        return len(self._redo_stack)