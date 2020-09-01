"""This module contains global settings."""

from sqlalchemy.ext.declarative import declarative_base

from utils.data_base_manager import DataBaseManager

ROUTE_MAX_LENGTH = 4

Base = declarative_base()

INPUT_DB_MANAGER = DataBaseManager()
OUTPUT_DB_MANAGER = DataBaseManager()

INPUT_ENGINE = r'sqlite:///C:\Development\Python\railway_infrastructure_test\obiekt_kolejowy.tdb2'
OUTPUT_ENGINE = r'sqlite:///C:\Development\Python\railway_infrastructure_test\output.tdb2'
