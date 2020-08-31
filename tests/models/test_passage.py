"""This module contains TestPassage class performing Passage class testing."""

from typing import TYPE_CHECKING
from unittest import TestCase

from sqlalchemy import create_engine, Table, MetaData, Integer, Column, String
from sqlalchemy.orm import sessionmaker

from models.passage import Passage

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine
    from sqlalchemy.orm import Session


class TestPassage(TestCase):
    """Passage class testing."""

    engine: 'Engine'
    session: 'Session'
    table: Table
    passage_1: Passage
    passage_2: Passage

    def _create_table(self):
        metadata = MetaData(self.engine)
        self.table = Table('przebiegi', metadata,
                           Column('id', Integer, primary_key=True),
                           Column('semafor_poczatkowy', String),
                           Column('semafor_koncowy', String))
        metadata.create_all()

    def _drop_table(self):
        self.table.drop()

    def _add_passages(self):
        self.passage_1 = Passage(1, 'semafor_1', 'semafor_2')
        self.passage_2 = Passage(2, 'semafor_2', 'semafor_3')

        self.session.add_all([self.passage_1, self.passage_2])
        self.session.commit()

    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = create_engine('sqlite:///:memory:')
        cls.session_maker = sessionmaker(cls.engine)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.engine.dispose()

    def setUp(self) -> None:
        self.session = self.session_maker()
        self._create_table()
        self._add_passages()

    def tearDown(self) -> None:
        self._drop_table()
        self.session.close()

    def test_parent_relationship_none_for_non_parent_passage(self):
        passage_id = 1
        passage: Passage = self.session.query(Passage).filter_by(id=passage_id).first()

        parent = passage.parent

        self.assertIsNone(parent, 'Does not return None for non-parent passage')

    def test_parent_relationship(self):
        passage_id = 2
        passage: Passage = self.session.query(Passage).filter_by(id=passage_id).first()
        expected_passage = self.passage_1

        parent = passage.parent

        self.assertIsNotNone(parent, 'Does not return parent for passage with parent')
        self.assertIs(expected_passage, parent, 'Parent does not equal the expected passage')

    def test_child_relationship(self):
        passage_id = 1
        passage: Passage = self.session.query(Passage).filter_by(id=passage_id).first()
        expected_passage = self.passage_2

        child = passage.child

        self.assertIsNotNone(child, 'Does not return child for passage with child')
        self.assertIs(expected_passage, child, 'Child does not equal the expected passage')

    def test_child_relationship_none_for_non_child_passage(self):
        passage_id = 2
        passage: Passage = self.session.query(Passage).filter_by(id=passage_id).first()

        child = passage.child

        self.assertIsNone(child, 'Does not return None for non-child passage')
