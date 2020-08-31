"""
This module contains PassageEstablishingResult class representing single passage establishing
validation result.
"""

from validation.results.passage.passage_result import PassageResult


class PassageEstablishingResult(PassageResult):
    """Represents single passage establishing validation result"""

    def get_result_log(self) -> str:
        """Returns log based on validation result."""
        return self._result_log_generator.get_establishing_passed_log() if self.result \
            else self._result_log_generator.get_establishing_failed_log()
