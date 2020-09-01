"""
This module contains EstablishingValidationAction class responsible for establishing state
validation.
"""
from typing import TYPE_CHECKING

from validation.railway_controller_panel import establish_passage
from validation.signal_state_model import SignalStateModel
from validation.actions.validation_action import ValidationAction
from validation.results.passage.passage_establishing_result import PassageEstablishingResult

if TYPE_CHECKING:
    from typing import Callable, Type


class EstablishingValidationAction(ValidationAction):
    """Responsible for a specific Passage establishing state validation."""

    @property
    def _controller_panel_func(self) -> 'Callable[[int], None]':
        """Railway Controller Panel establish_passage function reference."""
        return establish_passage

    @property
    def _result_class(self) -> 'Type[PassageEstablishingResult]':
        """Returns EstablishingResult class type."""
        return PassageEstablishingResult

    def _validate_states(self, start_signal_state: str, end_signal_state: str) -> bool:
        """Validates signals states."""
        return start_signal_state == SignalStateModel.SX \
            and end_signal_state == SignalStateModel.S1
