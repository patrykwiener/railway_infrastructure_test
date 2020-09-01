"""This module contains RouteService responsible for Route class logic."""

from typing import TYPE_CHECKING

from src.models.non_relational.route import Route

if TYPE_CHECKING:
    from typing import List
    from src.models.passage import Passage
    from src.services.passage_service import PassageService


class RouteService:
    """Represents service for Route class."""

    def __init__(self, passage_service: 'PassageService', route_max_length: int):
        self._passage_service = passage_service
        self._route_max_length = route_max_length

    def _get_route(self, root_passage: 'Passage') -> Route:
        """
        Constructs a route basing on root_passage.

        :param root_passage: route starting node
        :return: route containing found linked passages
        """
        linked_passages = self._passage_service.get_linked_passages(root_passage,
                                                                    self._route_max_length)
        return Route(linked_passages)

    def get_all_routes(self) -> 'List[Route]':
        """
        Creates routes from all found root passages.

        :return: list of routes
        """
        root_passages = self._passage_service.get_all_root_passages()
        return [self._get_route(root_passage) for root_passage in root_passages]
