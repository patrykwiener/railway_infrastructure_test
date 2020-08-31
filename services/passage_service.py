"""This module contains PassageService responsible for Passage model class logic."""

from typing import TYPE_CHECKING

from models.passage import Passage

if TYPE_CHECKING:
    from typing import List
    from sqlalchemy.orm import Session


class PassageService:
    """Represents service for Passage model class."""

    def __init__(self, session: 'Session'):
        self._session = session

    def get_all_root_passages(self) -> 'List[Passage]':
        """Returns all root passages."""
        return self._session.query(Passage) \
            .filter_by(parent=None) \
            .all()

    @staticmethod
    def get_linked_passages(root_passage: Passage, max_depth: int) -> 'List[Passage]':
        """
        Creates list of linked passages. Traverse recursively down the route hierarchy using
        Passage recursive relationship.

        :param root_passage: starting node
        :param max_depth: traversing max depth through the hierarchy
        :return: list of linked passages where the first element is the starting node
        """

        def get_linked_passages_internal(passage: Passage, array: 'List[Passage]',
                                         curr_depth: int):
            array.append(passage)
            passage = passage.child
            if not passage or curr_depth == max_depth:
                return array
            return get_linked_passages_internal(passage, array, curr_depth + 1)

        return get_linked_passages_internal(root_passage, [], 1)
