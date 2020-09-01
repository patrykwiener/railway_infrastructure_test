"""This module contains Results model class defining database's 'results' table"""

from sqlalchemy import Column, Integer, String

from settings import Base


class Results(Base):
    """Defines 'results' table."""

    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    route_passage_ids = Column(String)
    test_result = Column(String)
    test_log = Column(String)

    def __init__(self, route_passage_ids: str, test_result: str, test_log: str):
        self.route_passage_ids = route_passage_ids
        self.test_result = test_result
        self.test_log = test_log
