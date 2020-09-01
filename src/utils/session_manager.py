"""
This module contains session_manager context manager providing transactional session behaviour.
"""
from contextlib import contextmanager
from typing import TYPE_CHECKING

from sqlalchemy.exc import SQLAlchemyError

if TYPE_CHECKING:
    from sqlalchemy.orm import sessionmaker, Session


@contextmanager
def session_manager(session_maker: 'sessionmaker') -> 'Session':
    """
    Creates a session based on a given session_maker. Provides transactional behaviour.

    :param session_maker: session maker instance
    :return: session instance
    """
    session = session_maker()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        raise err
    finally:
        session.close()
