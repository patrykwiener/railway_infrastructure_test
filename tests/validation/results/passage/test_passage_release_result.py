"""
This module contains TestPassageReleaseResult class performing PassageReleaseResult
class testing.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.validation.results.passage.passage_release_result import PassageReleaseResult


class TestPassageReleaseResult(TestCase):
    """PassageReleaseResult class testing."""

    def _create_passage_release_result(self, result: bool):
        return PassageReleaseResult(
            self.passage_mock,
            self.start_semaphore_state,
            self.end_semaphore_state,
            result
        )

    def setUp(self) -> None:
        self.passage_mock = MagicMock()
        self.start_semaphore_state = 'State1'
        self.end_semaphore_state = 'State2'
        self.passed_passage_result = self._create_passage_release_result(True)
        self.failed_passage_result = self._create_passage_release_result(False)

    @patch('src.validation.results.passage.passage_result.ResultLogGenerator')
    def test_get_result_log_calls_passed_log_method(self, result_log_generator_mock):
        expected_return_value = 'test_string'
        result_log_generator_mock.return_value \
            .get_release_passed_log.return_value = expected_return_value

        actual = self.passed_passage_result.get_result_log()

        result_log_generator_mock.assert_called_once()
        result_log_generator_mock.return_value.get_release_passed_log.assert_called_once()
        result_log_generator_mock.return_value.get_release_failed_log.assert_not_called()
        self.assertEqual(actual, expected_return_value, 'Does not return the expected value')

    @patch('src.validation.results.passage.passage_result.ResultLogGenerator')
    def test_get_result_log_calls_failed_log_method(self, result_log_generator_mock):
        expected_return_value = 'test_string'
        result_log_generator_mock.return_value \
            .get_release_failed_log.return_value = expected_return_value

        actual = self.failed_passage_result.get_result_log()

        result_log_generator_mock.assert_called_once()
        result_log_generator_mock.return_value.get_release_passed_log.assert_not_called()
        result_log_generator_mock.return_value.get_release_failed_log.assert_called_once()
        self.assertEqual(actual, expected_return_value, 'Does not return the expected value')
