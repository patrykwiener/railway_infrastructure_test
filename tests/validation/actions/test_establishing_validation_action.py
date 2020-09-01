"""
This module contains TestEstablishingValidationAction class performing
EstablishingValidationAction class testing.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from validation.signal_state_model import SignalStateModel
from validation.actions.establishing_validation_action import EstablishingValidationAction


class TestEstablishingValidationAction(TestCase):
    """EstablishingValidationAction class testing."""

    def setUp(self) -> None:
        self.passage_mock = MagicMock()
        self.establishing_validation_action = EstablishingValidationAction(self.passage_mock)

    @patch.object(EstablishingValidationAction, '_result_class')
    @patch('validation.actions.validation_action.get_signal_state')
    @patch('validation.actions.establishing_validation_action.establish_route')
    def test_controller_panel_func_calls_establish_route_func(self, establish_route_mock, *args):
        self.establishing_validation_action.execute()
        establish_route_mock.assert_called_once_with(self.passage_mock.id)

    @patch('validation.actions.establishing_validation_action.establish_route')
    @patch.object(EstablishingValidationAction, '_result_class', new_callable=PropertyMock)
    @patch.object(EstablishingValidationAction, '_get_signal_states')
    def test_execute_returns_expected_results(self, get_signal_states_mock, result_class_mock,
                                              *args):
        states = [
            ((SignalStateModel.S1, SignalStateModel.SX), False),
            ((SignalStateModel.S1, SignalStateModel.S1), False),
            ((SignalStateModel.SX, SignalStateModel.SX), False),
            ((SignalStateModel.SX, SignalStateModel.S1), True)
        ]
        for value, expected_result in states:
            start_state, end_state = value
            get_signal_states_mock.return_value = value
            with self.subTest():
                self.establishing_validation_action.execute()
                result_class_mock.assert_called()
                result_class_mock.return_value.assert_called_with(self.passage_mock, start_state,
                                                                  end_state, expected_result)
