"""This module contains TestRoute class performing Route class testing."""
from unittest import TestCase
from unittest.mock import MagicMock

from models.non_relational.route import Route


class TestRoute(TestCase):
    """Route class testing."""

    def setUp(self) -> None:
        self.passages = [MagicMock(), MagicMock()]
        self.route = Route(self.passages)

    def test_passages_property_returns_passage_list(self):
        expected = self.passages
        actual = self.route.passages
        self.assertEqual(actual, expected, 'Property does not return route\'s passages')

    def test_reversed_passages_property_returns_reversed_passage_list(self):
        expected = self.passages[::-1]
        actual = self.route.reversed_passages
        self.assertEqual(actual, expected,
                         'Property does not return route\'s passages in revesed order')
