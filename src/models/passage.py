"""This module contains Passage model class reflecting database's 'przebiegi' table."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship

from src.settings import Base


class Passage(Base):
    """Reflects 'przebiegi' table. Implements parent and child recursive relationships."""

    __tablename__ = 'przebiegi'

    id = Column(Integer, primary_key=True)
    start_semaphore = Column('semafor_poczatkowy', String)
    end_semaphore = Column('semafor_koncowy', String, ForeignKey('przebiegi.semafor_poczatkowy'))

    child = relationship('Passage', remote_side=[start_semaphore], uselist=False)
    parent = relationship('Passage',
                          backref=backref('child_back_rel', remote_side=[start_semaphore]),
                          uselist=False)

    def __init__(self, _id: int, start_semaphore: str, end_semaphore: str):
        self.id = _id
        self.start_semaphore = start_semaphore
        self.end_semaphore = end_semaphore
