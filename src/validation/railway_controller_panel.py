"""This module contains railway controller panel interface mocks."""

import logging
import random

from src.validation.signal_state_model import SignalStateModel

logger = logging.getLogger(__name__)


def establish_passage(_id: int):
    """Mocks establishing passage action."""
    logger.info('trying to establish passage %s!', _id)


def release_passage(_id: int):
    """Mocks release passage action."""
    logger.info('trying to release passage %s!', _id)


def get_signal_state(name: str):
    """Mocks passage signal state."""
    return random.choice([SignalStateModel.SX, SignalStateModel.S1])
