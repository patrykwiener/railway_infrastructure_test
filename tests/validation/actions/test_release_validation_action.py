"""
This module contains TestReleaseValidationAction class performing ReleaseValidationAction
class testing.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from signal_state_model import SignalStateModel
from validation.actions.release_validation_action import ReleaseValidationAction


class TestReleaseValidationAction(TestCase):
    """ReleaseValidationAction class testing."""

    def setUp(self) -> None:
        self.passage_mock = MagicMock()
        self.release_validation_action = ReleaseValidationAction(self.passage_mock)

    @patch.object(ReleaseValidationAction, '_result_class')
    @patch('validation.actions.validation_action.get_signal_state')
    @patch('validation.actions.release_validation_action.release_route')
    def test_controller_panel_func_calls_release_route_func(self, release_route_mock, *args):
        self.release_validation_action.execute()
        release_route_mock.assert_called_once_with(self.passage_mock.id)

    @patch('validation.actions.release_validation_action.release_route')
    @patch.object(ReleaseValidationAction, '_result_class', new_callable=PropertyMock)
    @patch.object(ReleaseValidationAction, '_get_signal_states')
    def test_execute_returns_expected_results(self, get_signal_states_mock, result_class_mock,
                                              *args):
        states = [
            ((SignalStateModel.S1, SignalStateModel.SX), False),
            ((SignalStateModel.S1, SignalStateModel.S1), True),
            ((SignalStateModel.SX, SignalStateModel.SX), False),
            ((SignalStateModel.SX, SignalStateModel.S1), False)
        ]
        for value, expected_result in states:
            start_state, end_state = value
            get_signal_states_mock.return_value = value
            with self.subTest():
                self.release_validation_action.execute()
                result_class_mock.assert_called()
                result_class_mock.return_value.assert_called_with(self.passage_mock, start_state,
                                                                  end_state, expected_result)
