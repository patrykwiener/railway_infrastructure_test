from unittest import TestCase
from unittest.mock import MagicMock, patch

from signal_state_model import SignalStateModel
from validation.actions.release_validation_action import ReleaseValidationAction


class TestReleaseValidationAction(TestCase):

    def setUp(self) -> None:
        self.passage_mock = MagicMock()
        self.release_validation_action = ReleaseValidationAction(self.passage_mock)

    @patch('validation.actions.validation_action.get_signal_state')
    def test_get_signal_states_calls_signal_state_func(self, get_signal_state_mock):
        self.release_validation_action.execute()
        self.assertEqual(get_signal_state_mock.call_count, 2)
        get_signal_state_mock.assert_any_call(self.passage_mock.start_semaphore)
        get_signal_state_mock.assert_any_call(self.passage_mock.end_semaphore)

    @patch('validation.actions.release_validation_action.release_route')
    def test_controller_panel_func_calls_release_route_func(self, release_route_mock):
        self.release_validation_action.execute()
        release_route_mock.assert_called_once_with(self.passage_mock.id)

    def test_execute_returns_expected_results(self):
        states = [
            ((SignalStateModel.S1, SignalStateModel.SX), False),
            ((SignalStateModel.S1, SignalStateModel.S1), True),
            ((SignalStateModel.SX, SignalStateModel.SX), False),
            ((SignalStateModel.SX, SignalStateModel.S1), False)
        ]
        for value, expected in states:
            self.release_validation_action._get_signal_states = MagicMock(return_value=value)
            with self.subTest():
                result = self.release_validation_action.execute()
                self.assertEqual(result.result, expected)
