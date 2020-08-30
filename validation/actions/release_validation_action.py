"""This module contains ReleaseValidationAction class responsible for release state validation."""
from typing import TYPE_CHECKING

from railway_controller_panel import release_route
from signal_state_model import SignalStateModel
from validation.actions.validation_action import ValidationAction
from validation.results.release_result import ReleaseResult

if TYPE_CHECKING:
    from typing import Callable, Type


class ReleaseValidationAction(ValidationAction):
    """Responsible for a specific Passage release state validation."""

    @property
    def _controller_panel_func(self) -> 'Callable[[int], None]':
        """Railway Controller Panel release_route function reference."""
        return release_route

    @property
    def _result_class(self) -> 'Type[ReleaseResult]':
        """Returns ReleaseResult class type."""
        return ReleaseResult

    def _validate_states(self, start_signal_state: str, end_signal_state: str) -> bool:
        """Validates signals states."""
        return start_signal_state == SignalStateModel.S1 \
            and end_signal_state == SignalStateModel.S1
