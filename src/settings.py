"""This module contains global settings."""

from sqlalchemy.ext.declarative import declarative_base

from src.utils.data_base_manager import DataBaseManager

ROUTE_MAX_LENGTH = 4

Base = declarative_base()

INPUT_DB_MANAGER = DataBaseManager()
OUTPUT_DB_MANAGER = DataBaseManager()

ROOT_LOGGER_MODULE = ''

INPUT_TABLE_NAME = 'przebiegi'
OUTPUT_TABLE_NAME = 'results'
