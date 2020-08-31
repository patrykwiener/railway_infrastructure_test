"""This module contains TestPassageResult class performing PassageResult class testing."""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from validation.results.passage.passage_result import PassageResult


class TestPassageResult(TestCase):
    """PassageResult class testing."""

    def setUp(self) -> None:
        self.passage_mock = MagicMock()
        self.start_semaphore_state = 'State1'
        self.end_semaphore_state = 'State2'
        self.result = True

    @patch.object(PassageResult, '__abstractmethods__', set())
    def test_properties_returns_expected_values(self):
        passage_result = PassageResult(self.passage_mock, self.start_semaphore_state,
                                       self.end_semaphore_state, self.result)

        self.assertEqual(passage_result.passage, self.passage_mock)
        self.assertEqual(passage_result.start_semaphore_state, self.start_semaphore_state)
        self.assertEqual(passage_result.end_semaphore_state, self.end_semaphore_state)
        self.assertEqual(passage_result.result, self.result)
