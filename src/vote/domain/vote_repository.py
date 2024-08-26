from abc import ABC, abstractmethod
from typing import Any

from src.vote.domain.vote import Vote


class VoteRepository(ABC):
    @abstractmethod
    def save(self, vote: Vote) -> None:
        pass

    @abstractmethod
    def get_vote_log(self, vote: Vote) -> None:
        pass