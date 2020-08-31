"""
This module contains ResultLogGenerator util class responsible for generating validation result
logs.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from validation.results.passage.passage_result import PassageResult


class ResultLogGenerator:
    """Util class implementing validation result logs generation."""

    _PASSAGE_MSG = '{result} on {action} passage id: {id}; ' \
                   'start semaphore: {start_semaphore} - {start_semaphore_state}; ' \
                   'end semaphore: {end_semaphore} - {end_semaphore_state}.'
    _ESTABLISHING = 'establishing'
    _RELEASING = 'releasing'
    _FAILED = 'Failed'
    _PASSED = 'Passed'

    def __init__(self, passage_result: 'PassageResult'):
        self._passage_result = passage_result

    def _get_log(self, result: str, action: str) -> str:
        return self._PASSAGE_MSG.format(
            result=result,
            action=action,
            id=self._passage_result.passage.id,
            start_semaphore=self._passage_result.passage.start_semaphore,
            start_semaphore_state=self._passage_result.start_semaphore_state,
            end_semaphore=self._passage_result.passage.end_semaphore,
            end_semaphore_state=self._passage_result.end_semaphore_state
        )

    def get_establishing_failed_log(self) -> str:
        """Returns establishing validation failed log."""
        return self._get_log(self._FAILED, self._ESTABLISHING)

    def get_release_failed_log(self) -> str:
        """Returns release validation failed log."""
        return self._get_log(self._FAILED, self._RELEASING)

    def get_establishing_passed_log(self) -> str:
        """Returns establishing validation passed log."""
        return self._get_log(self._PASSED, self._ESTABLISHING)

    def get_release_passed_log(self) -> str:
        """Returns release validation passed log."""
        return self._get_log(self._PASSED, self._RELEASING)
