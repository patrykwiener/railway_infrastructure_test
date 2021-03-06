"""This module contains ReleaseValidationAction class responsible for release state validation."""
from typing import TYPE_CHECKING

from src.validation.actions.validation_action import ValidationAction
from src.validation.railway_controller_panel import release_passage
from src.validation.results.passage.passage_release_result import PassageReleaseResult
from src.validation.signal_state_model import SignalStateModel

if TYPE_CHECKING:
    from typing import Callable, Type


class ReleaseValidationAction(ValidationAction):
    """Responsible for a specific Passage release state validation."""

    @property
    def _controller_panel_func(self) -> 'Callable[[int], None]':
        """Railway Controller Panel release_passage function reference."""
        return release_passage

    @property
    def _result_class(self) -> 'Type[PassageReleaseResult]':
        """Returns ReleaseResult class type."""
        return PassageReleaseResult

    def _validate_states(self, start_signal_state: str, end_signal_state: str) -> bool:
        """Validates signals states."""
        return start_signal_state == SignalStateModel.S1 \
            and end_signal_state == SignalStateModel.S1
