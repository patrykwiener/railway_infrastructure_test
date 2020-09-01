"""This module contains TestResultsService class performing ResultsService class testing."""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.services.results_service import ResultsService


class TestResultsService(TestCase):
    """ResultsService class testing."""

    def setUp(self) -> None:
        self.session = MagicMock()
        self.result_service = ResultsService(self.session)
        self.route_results = MagicMock()

    @patch.object(ResultsService, '_get_route_passage_ids')
    @patch.object(ResultsService, '_get_test_result_as_string')
    @patch('src.services.results_service.Results')
    def test_save_route_results_creates_results(self, results_mock, get_test_result_as_string,
                                                get_route_passage_ids):
        self.result_service.save_route_results(self.route_results)

        results_mock.assert_called_once_with(
            get_route_passage_ids.return_value,
            get_test_result_as_string.return_value,
            self.route_results.get_results_log.return_value
        )

        results = results_mock.return_value
        self.session.add.assert_called_once_with(results)

    @patch.object(ResultsService, '_get_route_passage_ids')
    @patch('src.services.results_service.Results')
    def test_save_route_results_created_with_proper_test_result(self, results_mock,
                                                                get_route_passage_ids):
        value_expected_list = [
            (True, 'PASS'),
            (False, 'FAIL'),
        ]
        for value, expected in value_expected_list:
            with self.subTest():
                self.route_results.get_bool_result.return_value = value
                expected_test_result_str = expected

                self.result_service.save_route_results(self.route_results)
                results_mock.assert_called_with(
                    get_route_passage_ids.return_value,
                    expected_test_result_str,
                    self.route_results.get_results_log.return_value
                )

    @patch.object(ResultsService, '_get_test_result_as_string')
    @patch('src.services.results_service.Results')
    def test_save_route_results_get_proper_passage_ids(self, results_mock,
                                                       get_test_result_as_string):
        passage_1 = MagicMock()
        passage_1.id = '1'
        passage_2 = MagicMock()
        passage_2.id = '2'
        self.route_results.route.passages = [passage_1, passage_2]
        expected_route_passage_ids_str = '1;2'

        self.result_service.save_route_results(self.route_results)

        results_mock.assert_called_once_with(
            expected_route_passage_ids_str,
            get_test_result_as_string.return_value,
            self.route_results.get_results_log.return_value
        )
