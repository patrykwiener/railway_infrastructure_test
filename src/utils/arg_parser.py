"""This module contains ArgumentParserWrapper implementing command-line arguments parsing."""
import argparse


class ArgumentParserWrapper:
    """Implements command-line arguments parsing."""

    _DESCRIPTION = 'Railway infrastructure test performing railway object signal states ' \
                   'validation. '

    def __init__(self):
        self._parser = argparse.ArgumentParser(description=self._DESCRIPTION)
        self.input_db_url = None
        self.output_db_url = None
        self.route_max_length = None

    def _parse_input_database(self):
        self._parser.add_argument(
            '-in',
            '--input_database',
            help='railway object infrastructure database url containing table \'przebiegi\' with '
                 'test data',
            required=True,
        )

    def _parse_output_database(self):
        self._parser.add_argument(
            '-out',
            '--output_database',
            help='existing or not results database url',
            required=True,
        )

    def _parse_route_max_length(self):
        self._parser.add_argument(
            '-r',
            '--route_max_length',
            help='route max length',
        )

    def parse_arguments(self):
        """Performs arguments parsing."""
        self._parse_input_database()
        self._parse_output_database()
        self._parse_route_max_length()
        parsed_args = self._parser.parse_args()
        self.input_db_url = parsed_args.input_database
        self.output_db_url = parsed_args.output_database
        self.route_max_length = int(parsed_args.route_max_length)
