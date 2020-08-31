"""This module contains PassageResult base class representing single passage validation result."""

from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

from validation.utils.result_log_generator import ResultLogGenerator

if TYPE_CHECKING:
    from models.passage import Passage


@dataclass(frozen=True)
class PassageResult(ABC):
    """Represents single passage validation result."""

    passage: 'Passage'
    start_semaphore_state: str
    end_semaphore_state: str
    result: bool

    @property
    def _result_log_generator(self) -> ResultLogGenerator:
        return ResultLogGenerator(self)

    @abstractmethod
    def get_result_log(self) -> str:
        """Returns result log."""
