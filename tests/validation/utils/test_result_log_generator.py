"""This module contains TestResultLogGenerator class performing PassageResult class testing."""
from unittest import TestCase
from unittest.mock import MagicMock

from validation.utils.result_log_generator import ResultLogGenerator


class TestResultLogGenerator(TestCase):
    """ResultLogGenerator class testing."""

    def _create_passage_result_mock(self):
        passage_result_mock = MagicMock()
        passage_result_mock.passage.id = self.idx
        passage_result_mock.passage.start_semaphore = self.start_semaphore
        passage_result_mock.start_semaphore_state = self.start_semaphore_state
        passage_result_mock.passage.end_semaphore = self.end_semaphore
        passage_result_mock.end_semaphore_state = self.end_semaphore_state
        return passage_result_mock

    def setUp(self) -> None:
        self.idx = 1
        self.start_semaphore = 'start_semaphore'
        self.start_semaphore_state = 'State1'
        self.end_semaphore = 'end_semaphore'
        self.end_semaphore_state = 'State2'

        self.passage_result_mock = self._create_passage_result_mock()
        self.result_log_generator = ResultLogGenerator(self.passage_result_mock)

        self.expected_log_template = f'{{result}} on {{action}} passage id: {self.idx}; ' \
                                     f'start semaphore: {self.start_semaphore} - ' \
                                     f'{self.start_semaphore_state}; end semaphore: ' \
                                     f'{self.end_semaphore} - {self.end_semaphore_state}.'

    def test_get_establishing_failed_log(self):
        expected = self.expected_log_template.format(result='Failed', action='establishing')
        actual = self.result_log_generator.get_establishing_failed_log()
        self.assertEqual(expected, actual, 'Does not return expected log')

    def test_get_release_failed_log(self):
        expected = self.expected_log_template.format(result='Failed', action='releasing')
        actual = self.result_log_generator.get_release_failed_log()
        self.assertEqual(expected, actual, 'Does not return expected log')

    def test_get_establishing_passed_log(self):
        expected = self.expected_log_template.format(result='Passed', action='establishing')
        actual = self.result_log_generator.get_establishing_passed_log()
        self.assertEqual(expected, actual, 'Does not return expected log')

    def test_get_release_passed_log(self):
        expected = self.expected_log_template.format(result='Passed', action='releasing')
        actual = self.result_log_generator.get_release_passed_log()
        self.assertEqual(expected, actual, 'Does not return expected log')
