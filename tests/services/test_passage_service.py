"""This module contains TestPassageService class performing PassageService class testing."""

from typing import TYPE_CHECKING
from unittest import TestCase

from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.passage import Passage
from src.services.passage_service import PassageService

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


class TestPassageService(TestCase):
    """PassageService class testing."""

    engine: 'Engine'

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
        self.passage_3 = Passage(3, 'semafor_6', 'semafor_7')

        self.session.add_all([self.passage_1, self.passage_2, self.passage_3])
        self.session.commit()

    def _add_circular_passages(self):
        self.passage_1 = Passage(1, 'semafor_1', 'semafor_2')
        self.passage_2 = Passage(2, 'semafor_2', 'semafor_3')
        self.passage_3 = Passage(3, 'semafor_3', 'semafor_1')

        self.session.add_all([self.passage_1, self.passage_2, self.passage_3])
        self.session.commit()

    def _add_forked_passages(self):
        self.passage_1 = Passage(1, 'semafor_1', 'semafor_2')
        self.passage_2 = Passage(2, 'semafor_2', 'semafor_3')
        self.passage_3 = Passage(3, 'semafor_2', 'semafor_4')

        self.session.add_all([self.passage_1, self.passage_2, self.passage_3])
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
        self._passage_service = PassageService(self.session)

    def tearDown(self) -> None:
        self._drop_table()
        self.session.close()

    def test_get_all_root_passages(self):
        self._add_passages()
        expected = [self.passage_1, self.passage_3]

        passages = self._passage_service.get_all_root_passages()

        self.assertEqual(len(expected), len(passages), 'Returns to many passages')
        self.assertIs(expected[0], passages[0],
                      'First root passage does not equal the expected one')
        self.assertIs(expected[1], passages[1],
                      'Second root passage does not equal the expected one')

    def test_get_all_root_passages_with_circular_route(self):
        self._add_circular_passages()

        passages = self._passage_service.get_all_root_passages()

        self.assertFalse(passages, 'Root passage is not empty on circular route')

    def test_get_linked_passages(self):
        self._add_passages()
        root = self.passage_1
        max_depth = 4
        expected = [self.passage_1, self.passage_2]

        linked_passages = self._passage_service.get_linked_passages(root, max_depth)

        self.assertEqual(len(expected), len(linked_passages), 'Returns to many passages')
        self.assertEqual(expected[0], linked_passages[0],
                         'First passage does not equal the expected one')
        self.assertEqual(expected[1], linked_passages[1],
                         'Second passage does not equal the expected one')

    def test_get_linked_passages_with_exceeded_max_depth(self):
        self._add_passages()
        root = self.passage_1
        max_depth = 1
        expected = [self.passage_1]

        linked_passages = self._passage_service.get_linked_passages(root, max_depth)

        self.assertEqual(len(expected), len(linked_passages), 'Returns to many passages')
        self.assertEqual(expected[0], linked_passages[0],
                         'First passage does not equal the expected one')

    def test_get_linked_passages_with_fork_in_road(self):
        self._add_forked_passages()
        root = self.passage_1
        max_depth = 4
        expected = [self.passage_1, self.passage_2]
        expected_length = len(expected)

        passages = self._passage_service.get_linked_passages(root, max_depth)

        self.assertEqual(len(passages), expected_length, 'Does not ignore forked passages')
        self.assertIs(expected[0], passages[0],
                      'First root passage does not equal the expected one')
        self.assertIs(expected[1], passages[1],
                      'Second root passage does not equal the expected one')
