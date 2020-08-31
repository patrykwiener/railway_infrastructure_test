"""
This module contains RouteResults class responsible for interpreting whole route validation result.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.non_relational.route import Route
    from typing import List
    from validation.results.passage.passage_establishing_result import PassageEstablishingResult
    from validation.results.passage.passage_release_result import PassageReleaseResult
    from validation.results.passage.passage_result import PassageResult


class RouteResults:
    """Responsible for storing and interpreting whole route validation result."""

    _RESULTS_LOG_SEP = ' '

    def __init__(self,
                 route: 'Route',
                 establishing_results: 'List[PassageEstablishingResult]',
                 release_results: 'List[PassageReleaseResult]'):
        self._route = route
        self._establishing_results = establishing_results
        self._release_results = release_results
        self._results: 'List[PassageResult]' = [*self._establishing_results,
                                                *self._release_results]

    @property
    def route(self) -> 'Route':
        """Returns route."""
        return self._route

    def get_bool_result(self) -> bool:
        """
        Validates whether whole route passed or not the validation.

        :return: True when all passages validation results both establishing end release are True,
        False otherwise.
        """
        return all(passage_result.result for passage_result in self._results)

    def get_results_log(self) -> str:
        """Returns string containing every passage validation result log."""
        return f'{self._RESULTS_LOG_SEP}'.join(
            [passage_result.get_result_log() for passage_result in self._results])
