"""This module contains TestRouteResults class performing RouteResults class testing."""
from unittest import TestCase
from unittest.mock import MagicMock

from src.validation.results.route_results import RouteResults


class TestRouteResults(TestCase):
    """RouteResults class testing."""

    def setUp(self) -> None:
        self.route = MagicMock()
        self.result_1 = MagicMock()
        self.result_2 = MagicMock()
        self.result_3 = MagicMock()
        self.result_4 = MagicMock()
        self.route_results = RouteResults(self.route, [self.result_1, self.result_2],
                                          [self.result_3, self.result_4])

    def test_route_returns_route(self):
        expected = self.route
        actual = self.route_results.route
        self.assertEqual(expected, actual, 'Does not return route passed in constructor')

    def test_get_bool_result_returns_true_when_all_passed(self):
        self.result_1.result = True
        self.result_2.result = True
        self.result_3.result = True
        self.result_4.result = True

        actual = self.route_results.get_bool_result()
        self.assertTrue(actual, 'Does not equal False on all passed')

    def test_get_bool_result_returns_false_when_any_failed(self):
        self.result_1.result = True
        self.result_2.result = True
        self.result_3.result = True
        self.result_4.result = False

        actual = self.route_results.get_bool_result()
        self.assertFalse(actual, 'Does not equal False on any failed')

    def test_get_results_log(self):
        results = [self.result_1, self.result_2, self.result_3, self.result_4]
        for result_mock in results:
            result_mock.get_result_log.return_value = 'some_log'

        expected = 'some_log some_log some_log some_log'
        actual = self.route_results.get_results_log()
        self.assertEqual(expected, actual, 'Does not equal expected log string')
        for result in results:
            result.get_result_log.assert_called_once()
