"""This module contains global settings."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

ROUTE_MAX_LENGTH = 4

INPUT_ENGINE = create_engine(
    r'sqlite:///C:\Development\Python\railway_infrastructure_test\obiekt_kolejowy.tdb2')
OUTPUT_ENGINE = create_engine(
    r'sqlite:///C:\Development\Python\railway_infrastructure_test\output.tdb2')
InputBase = declarative_base(INPUT_ENGINE)
OutputBase = declarative_base(OUTPUT_ENGINE)
