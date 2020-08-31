"""This module contains TestValidationAction class performing ValidationAction class testing."""

from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock

from validation.actions.validation_action import ValidationAction


class TestValidationAction(TestCase):
    """ValidationAction class testing."""

    def _create_validation_action_obj(self):
        return ValidationAction(self.passage_mock)

    def setUp(self) -> None:
        self.passage_mock = MagicMock()

    @patch('validation.actions.validation_action.get_signal_state')
    @patch.object(ValidationAction, '_result_class', new_callable=PropertyMock)
    @patch.object(ValidationAction, '_controller_panel_func', new_callable=PropertyMock)
    @patch.object(ValidationAction, '__abstractmethods__', set())
    def test_execute_calls_signal_state_func(self, controller_panel_func_mock,
                                             result_class_mock, get_signal_state_mock):
        validation_action = self._create_validation_action_obj()

        validation_action.execute()
        self.assertEqual(get_signal_state_mock.call_count, 2,
                         'get_signal_state function was not called 2 times')
        get_signal_state_mock.assert_any_call(self.passage_mock.start_semaphore)
        get_signal_state_mock.assert_any_call(self.passage_mock.end_semaphore)
        controller_panel_func_mock.assert_called_once()
        result_class_mock.assert_called_once()

    @patch.object(ValidationAction, '_result_class', new_callable=PropertyMock)
    @patch.object(ValidationAction, '_controller_panel_func', new_callable=PropertyMock)
    @patch.object(ValidationAction, '__abstractmethods__', set())
    def test_execute_returns_result_class_obj(self, controller_panel_func_mock, result_class_mock):
        expected_return_value = 'some_obj'
        result_class_mock.return_value.return_value = expected_return_value
        validation_action = self._create_validation_action_obj()

        result = validation_action.execute()

        controller_panel_func_mock.assert_called_once()
        result_class_mock.assert_called_once()
        result_class_mock.return_value.assert_called_once()
        self.assertEqual(expected_return_value, result)
