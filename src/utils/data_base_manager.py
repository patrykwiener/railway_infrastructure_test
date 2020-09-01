"""This class contains DataBaseManager class responsible for database management."""
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

logger = logging.getLogger(__name__)


class DataBaseNotExistsError(Exception):
    """Database does not exists."""


class TableNotExistsError(Exception):
    """Table does not exists."""


class DataBaseManager:
    """Provides database management operations."""

    def __init__(self):
        self._engine = None

    @property
    def session_maker(self) -> sessionmaker:
        """Returns session maker."""
        return sessionmaker(self._engine)

    def _check_if_table_exists(self, name: str) -> bool:
        """Returns True if table with a given name exists, False otherwise."""
        return self._engine.dialect.has_table(self._engine, name)

    def _check_if_database_exists(self):
        return database_exists(self._engine.url)

    def create_engine(self, url: str):
        """
        Creates database engine.

        :param url: database url
        """
        logger.info('setting up database: %s', url)
        self._engine = create_engine(url)

    def raise_if_database_not_exists(self):
        """
        Checks whether database exists.

        :raises DataBaseNotExistsError: when database with a given url does not exists
        """
        if not self._check_if_database_exists():
            raise DataBaseNotExistsError(f'Database: \'{self._engine.url}\' does not exists')

    def raise_if_table_not_exists(self, name: str):
        """
        Checks whether table with a given name exists.

        :raises TableNotExistsError: when table with a name url not exists
        """
        if not self._check_if_table_exists(name):
            raise TableNotExistsError(f'Table: \'{name}\' does not exists')

    def create_database_if_not_exists(self):
        """Creates database if nto exists from engine url."""
        if not self._check_if_database_exists():
            logger.info('creating database: %s', self._engine.url)
            create_database(self._engine.url)

    def create_table_if_not_exists(self, model, name: str):
        """
        Creates table if not exists.

        :param model: model class reflecting database table
        :param name: table name
        """
        if not self._check_if_table_exists(name):
            logger.info('creating table: %s', name)
            model.__table__.create(self._engine)
