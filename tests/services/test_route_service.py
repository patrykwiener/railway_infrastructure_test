"""This module contains TestRouteService class performing RouteService class testing."""
from unittest import TestCase
from unittest.mock import MagicMock

from src.services.route_service import RouteService


class TestRouteService(TestCase):
    """RouteService class testing."""

    def _create_passage_service_mock(self):
        self.passage_service_mock = MagicMock()

        self.linked_passages_mock = [MagicMock(), MagicMock()]
        self.passage_service_mock.get_linked_passages = MagicMock(
            return_value=self.linked_passages_mock)

        return self.passage_service_mock

    def setUp(self) -> None:
        self.passage_service_mock = self._create_passage_service_mock()
        self.route_max_length = MagicMock()
        self.route_service = RouteService(self.passage_service_mock, self.route_max_length)

    def test_get_all_routes(self):
        root_passages_mock = [MagicMock(), MagicMock()]
        self.passage_service_mock.get_all_root_passages = MagicMock(
            return_value=root_passages_mock)

        routes_number = 2

        routes = self.route_service.get_all_routes()

        self.assertEqual(len(routes), routes_number, 'Number of routes does not equal expected')
        self.assertEqual(routes[0].passages, self.linked_passages_mock,
                         'First Route does not contain linked passages')
        self.assertEqual(routes[1].passages, self.linked_passages_mock,
                         'Second Route does not contain linked passages')

        self.passage_service_mock.get_all_root_passages.assert_called_once_with()
        self.passage_service_mock.get_linked_passages.assert_any_call(root_passages_mock[0],
                                                                      self.route_max_length)
        self.passage_service_mock.get_linked_passages.assert_any_call(root_passages_mock[1],
                                                                      self.route_max_length)

    def test_get_all_routes_returns_empty_list(self):
        root_passages_mock = []
        self.passage_service_mock.get_all_root_passages = MagicMock(
            return_value=root_passages_mock)

        routes = self.route_service.get_all_routes()

        self.assertFalse(routes, 'Route list is not empty')
        self.passage_service_mock.get_all_root_passages.assert_called_once_with()
        self.passage_service_mock.get_linked_passages.assert_not_called()
