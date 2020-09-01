"""
This module contains ValidationAction abstract class implementing core logic responsible for
single Passage establishing and release state validation.
"""
from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

from src.validation.railway_controller_panel import get_signal_state

if TYPE_CHECKING:
    from typing import Callable, Tuple
    from src.models.passage import Passage


class ValidationAction(ABC):
    """Base class for single Passage establishing and release state validation."""

    def __init__(self, passage: 'Passage'):
        self._passage = passage

    @property
    @abstractmethod
    def _result_class(self):
        """Returns specific Result class type."""

    @property
    @abstractmethod
    def _controller_panel_func(self) -> 'Callable[[int], None]':
        """Railway Controller Panel function reference."""

    @abstractmethod
    def _validate_states(self, start_signal_state: str, end_signal_state: str) -> bool:
        """Validates signals states."""

    def _get_signal_states(self) -> 'Tuple[str, str]':
        """Returns tuple containing passage's semaphores states."""
        return get_signal_state(self._passage.start_semaphore), \
            get_signal_state(self._passage.end_semaphore)

    def execute(self):
        """
        Executes Passage state validation depended on inherited logic.

        :return: validation result
        """
        self._controller_panel_func(self._passage.id)
        start_signal_state, end_signal_state = self._get_signal_states()
        result = self._validate_states(start_signal_state, end_signal_state)
        return self._result_class(self._passage, start_signal_state, end_signal_state, result)
