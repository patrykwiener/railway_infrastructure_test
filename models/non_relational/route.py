"""This module contains Route class representing single railway route."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.passage import Passage
    from typing import List


class Route:
    """Represents single railway route constructed from multiple passages."""

    def __init__(self, passages: 'List[Passage]'):
        self._passages = passages

    @property
    def passages(self) -> 'List[Passage]':
        """Returns route's passages."""
        return self._passages

    @property
    def reversed_passages(self) -> 'List[Passage]':
        """Returns route's passages in reversed order."""
        return self._passages[::-1]
