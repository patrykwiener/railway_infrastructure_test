"""This module contains ResultsService responsible for Results model class logic."""

from typing import TYPE_CHECKING

from models.results import Results
from validation.results.route_results import RouteResults

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class ResultsService:
    """Represents service for Results model class."""

    _PASS = 'PASS'
    _FAIL = 'FAIL'

    _ROUTE_PASSAGE_IDS_SEP = ';'

    def __init__(self, session: 'Session'):
        self._session = session

    def _get_route_passage_ids(self, route_results: RouteResults) -> str:
        """Creates string containing whole route passage ids."""
        return f'{self._ROUTE_PASSAGE_IDS_SEP}'.join(
            [str(passage.id) for passage in route_results.route.passages])

    def _get_test_result_as_string(self, route_results: RouteResults) -> str:
        """Maps test bool result to string message."""
        return self._PASS if route_results.get_bool_result() else self._FAIL

    def save_route_results(self, route_results: RouteResults):
        """Saves route results to database."""
        results = Results(
            self._get_route_passage_ids(route_results),
            self._get_test_result_as_string(route_results),
            route_results.get_results_log(),
        )
        self._session.add(results)
