from dataclasses import dataclass

from models.passage import Passage


@dataclass(frozen=True)
class Result:
    passage: Passage
    start_semaphore_state: str
    end_semaphore_state: str
    result: bool
