"""This module contains App class defining for application main operations."""

import logging

from src import settings
from src.models.results import Results
from src.services.passage_service import PassageService
from src.services.results_service import ResultsService
from src.services.route_service import RouteService
from src.utils.arg_parser import ArgumentParserWrapper
from src.utils.session_manager import session_manager
from src.validation.route_validation_director import RouteValidationDirector

logger = logging.getLogger(__name__)


class App:
    """Defines application main operations."""

    def __init__(self):
        self.routes = None
        self.argument_parser = ArgumentParserWrapper()

    def parse_arguments(self):
        """Parses command-line arguments."""
        self.argument_parser.parse_arguments()

    def setup_input_database(self):
        """Sets up input database."""
        settings.INPUT_DB_MANAGER.create_engine(self.argument_parser.input_db_url)
        settings.INPUT_DB_MANAGER.raise_if_database_not_exists()
        settings.INPUT_DB_MANAGER.raise_if_table_not_exists(settings.INPUT_TABLE_NAME)

    def setup_output_database(self):
        """Sets up output database."""
        settings.OUTPUT_DB_MANAGER.create_engine(self.argument_parser.output_db_url)
        settings.OUTPUT_DB_MANAGER.create_database_if_not_exists()
        settings.OUTPUT_DB_MANAGER.create_table_if_not_exists(Results, settings.OUTPUT_TABLE_NAME)

    def fetch_routes(self):
        """Fetches routes from database."""
        if self.argument_parser.route_max_length:
            settings.ROUTE_MAX_LENGTH = self.argument_parser.route_max_length
        logger.info('fetching routes with max depth level: %s', settings.ROUTE_MAX_LENGTH)
        with session_manager(settings.INPUT_DB_MANAGER.session_maker) as session:
            passage_service = PassageService(session)
            route_service = RouteService(passage_service, settings.ROUTE_MAX_LENGTH)
            self.routes = route_service.get_all_routes()
        logger.info('found %s routes', len(self.routes))

    def perform_validation(self):
        """Performs every route validation."""
        logger.info('performing validation')
        for route in self.routes:
            result = RouteValidationDirector(route).validate()
            with session_manager(settings.OUTPUT_DB_MANAGER.session_maker) as session:
                ResultsService(session).save_route_results(result)
