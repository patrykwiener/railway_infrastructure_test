"""
This module contains TestEstablishingValidationAction class performing
EstablishingValidationAction class testing.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from signal_state_model import SignalStateModel
from validation.actions.establishing_validation_action import EstablishingValidationAction


class TestEstablishingValidationAction(TestCase):
    """EstablishingValidationAction class testing."""

    def setUp(self) -> None:
        self.passage_mock = MagicMock()
        self.establishing_validation_action = EstablishingValidationAction(self.passage_mock)

    @patch('validation.actions.validation_action.get_signal_state')
    def test_get_signal_states_calls_signal_state_func(self, get_signal_state_mock):
        self.establishing_validation_action.execute()
        self.assertEqual(get_signal_state_mock.call_count, 2,
                         'get_signal_state function was not called 2 times')
        get_signal_state_mock.assert_any_call(self.passage_mock.start_semaphore)
        get_signal_state_mock.assert_any_call(self.passage_mock.end_semaphore)

    @patch('validation.actions.establishing_validation_action.establish_route')
    def test_controller_panel_func_calls_establish_route_func(self, establish_route_mock):
        self.establishing_validation_action.execute()
        establish_route_mock.assert_called_once_with(self.passage_mock.id)

    def test_execute_returns_expected_results(self):
        states = [
            ((SignalStateModel.S1, SignalStateModel.SX), False),
            ((SignalStateModel.S1, SignalStateModel.S1), False),
            ((SignalStateModel.SX, SignalStateModel.SX), False),
            ((SignalStateModel.SX, SignalStateModel.S1), True)
        ]
        for value, expected in states:
            self.establishing_validation_action._get_signal_states = MagicMock(return_value=value)
            with self.subTest():
                result = self.establishing_validation_action.execute()
                self.assertEqual(result.result, expected, 'Result does not meet the expected')
