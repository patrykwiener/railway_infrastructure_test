"""This module contains App class defining for application main operations."""

import logging

from utils.session_manager import session_manager
from models.results import Results
from services.passage_service import PassageService
from services.results_service import ResultsService
from services.route_service import RouteService
from settings import OUTPUT_DB_MANAGER, INPUT_DB_MANAGER, ROUTE_MAX_LENGTH, OUTPUT_ENGINE, \
    INPUT_ENGINE
from validation.route_validation_director import RouteValidationDirector

logger = logging.getLogger(__name__)


class App:
    """Defines application main operations."""

    def __init__(self):
        self.routes = None

    def parse_arguments(self):
        """Parses command-line arguments."""
        logger.info('parsing input arguments')

    @staticmethod
    def setup_input_database():
        """Sets up input database."""
        INPUT_DB_MANAGER.create_engine(INPUT_ENGINE)

    @staticmethod
    def setup_output_database():
        """Sets up output database."""
        OUTPUT_DB_MANAGER.create_engine(OUTPUT_ENGINE)
        OUTPUT_DB_MANAGER.create_database_if_not_exists()
        OUTPUT_DB_MANAGER.create_table_if_not_exists(Results, 'results')

    def fetch_routes(self):
        """Fetches routes from database."""
        logger.info('fetching routes with max depth level: %s', ROUTE_MAX_LENGTH)
        with session_manager(INPUT_DB_MANAGER.session_maker) as session:
            passage_service = PassageService(session)
            route_service = RouteService(passage_service, ROUTE_MAX_LENGTH)
            self.routes = route_service.get_all_routes()
        logger.info('found %s routes', len(self.routes))

    def perform_validation(self):
        """Performs every route validation."""
        logger.info('performing validation')
        for route in self.routes:
            result = RouteValidationDirector(route).validate()
            with session_manager(OUTPUT_DB_MANAGER.session_maker) as session:
                ResultsService(session).save_route_results(result)
