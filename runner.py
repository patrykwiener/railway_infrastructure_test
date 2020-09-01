"""Main app runner."""

import logging

from app import App
from settings import ROOT_LOGGER_MODULE


def setup_info_level_logger():
    """Sets up logger."""
    logger = logging.getLogger(ROOT_LOGGER_MODULE)
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


if __name__ == '__main__':
    setup_info_level_logger()

    app = App()
    app.parse_arguments()
    app.setup_input_database()
    app.setup_output_database()
    app.fetch_routes()
    app.perform_validation()
