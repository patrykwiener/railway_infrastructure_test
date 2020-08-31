import random
import logging

from signal_state_model import SignalStateModel

logger = logging.getLogger(__name__)


def establish_route(_id: int):
    logger.info(f'trying to establish route {_id}!')


def release_route(_id: int):
    logger.info(f'trying to release route {_id}!')


def get_signal_state(name: str):
    return random.choice([SignalStateModel.SX, SignalStateModel.S1])
