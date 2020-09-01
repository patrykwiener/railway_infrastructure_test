"""
This module contains RouteValidationDirector class responsible for directing route validation.
"""
from typing import TYPE_CHECKING

from src.validation.actions.establishing_validation_action import EstablishingValidationAction
from src.validation.actions.release_validation_action import ReleaseValidationAction
from src.validation.results.route_results import RouteResults

if TYPE_CHECKING:
    from src.models.passage import Passage
    from src.validation.results.passage.passage_establishing_result import \
        PassageEstablishingResult
    from src.validation.results.passage.passage_release_result import PassageReleaseResult
    from src.models.non_relational.route import Route
    from src.validation.actions.validation_action import ValidationAction
    from typing import Type, List


class RouteValidationDirector:
    """Responsible for directing route validation."""

    def __init__(self, route: 'Route'):
        self._route = route

    @staticmethod
    def _perform_route_validation(passages: 'List[Passage]', action: 'Type[ValidationAction]'):
        """Performs validation on given route by executing given action."""
        return [action(passage).execute() for passage in passages]

    def _perform_establishing(self) -> 'List[PassageEstablishingResult]':
        """Performs establishing validation."""
        return self._perform_route_validation(self._route.passages, EstablishingValidationAction)

    def _perform_releasing(self) -> 'List[PassageReleaseResult]':
        """Performs release validation on reversed route."""
        return self._perform_route_validation(self._route.reversed_passages,
                                              ReleaseValidationAction)

    def validate(self) -> RouteResults:
        """
        Directs firstly establishing and then releasing whole route validation. The results stores
        in RouteResults object.

        :return: RouteResults object containing given route validation result
        """
        establishing_results = self._perform_establishing()
        release_results = self._perform_releasing()
        return RouteResults(self._route, establishing_results, release_results)
