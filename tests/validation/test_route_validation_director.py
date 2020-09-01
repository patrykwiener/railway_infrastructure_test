"""
This module contains TestRouteValidationDirector class performing RouteValidationDirector class
testing.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from src.validation.route_validation_director import RouteValidationDirector


class TestRouteValidationDirector(TestCase):
    """RouteValidationDirector class testing."""

    def setUp(self) -> None:
        self.passage_1 = MagicMock()
        self.passage_2 = MagicMock()
        self.passages = [self.passage_1, self.passage_2]

        self.route = MagicMock()
        self.route.passages = self.passages
        self.route.reversed_passages = self.passages[::-1]
        self.route_validation_director = RouteValidationDirector(self.route)

    @patch('src.validation.route_validation_director.RouteResults')
    @patch('src.validation.route_validation_director.EstablishingValidationAction')
    @patch('src.validation.route_validation_director.ReleaseValidationAction')
    def test_validate_performs_release_validation(self, release_validation_action_mock, *args):
        expected_release_validation_action_call_number = 2

        self.route_validation_director.validate()

        self.assertEqual(expected_release_validation_action_call_number,
                         release_validation_action_mock.call_count,
                         'Not called expected times')
        release_validation_action_mock.assert_any_call(self.passage_1)
        release_validation_action_mock.assert_any_call(self.passage_2)
        release_validation_action_mock.return_value.execute.assert_called()

    @patch('src.validation.route_validation_director.RouteResults')
    @patch('src.validation.route_validation_director.ReleaseValidationAction')
    @patch('src.validation.route_validation_director.EstablishingValidationAction')
    def test_validate_performs_establishing_validation(self, establishing_validation_action_mock,
                                                       *args):
        expected_establishing_validation_action_call_number = 2

        self.route_validation_director.validate()

        self.assertEqual(expected_establishing_validation_action_call_number,
                         establishing_validation_action_mock.call_count,
                         'Not called expected times')
        establishing_validation_action_mock.assert_any_call(self.passage_1)
        establishing_validation_action_mock.assert_any_call(self.passage_2)
        establishing_validation_action_mock.return_value.execute.assert_called()

    @patch.object(RouteValidationDirector, '_perform_releasing')
    @patch.object(RouteValidationDirector, '_perform_establishing')
    @patch('src.validation.route_validation_director.RouteResults')
    def test_validate_returns_route_results(self, route_results_mock, perform_establishing_mock,
                                            perform_releasing_mock):
        expected_perform_establishing_value = MagicMock()
        perform_establishing_mock.return_value = expected_perform_establishing_value
        expected_perform_releasing_value = MagicMock()
        perform_releasing_mock.return_value = expected_perform_releasing_value

        result = self.route_validation_director.validate()

        perform_establishing_mock.assert_called_once()
        perform_releasing_mock.assert_called_once()
        route_results_mock.assert_called_once_with(self.route, expected_perform_establishing_value,
                                                   expected_perform_releasing_value)

        self.assertEqual(route_results_mock.return_value, result, 'Does not return new object')
