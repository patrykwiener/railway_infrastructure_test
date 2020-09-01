"""
This module contains PassageReleaseResult class representing single passage release validation
result.
"""
from src.validation.results.passage.passage_result import PassageResult


class PassageReleaseResult(PassageResult):
    """Represents single passage release validation result"""

    def get_result_log(self) -> str:
        """Returns log based on validation result."""
        return self._result_log_generator.get_release_passed_log() if self.result \
            else self._result_log_generator.get_release_failed_log()
