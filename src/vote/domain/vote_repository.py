from abc import ABC, abstractmethod
from typing import Any

from src.vote.domain.vote import Vote
from src.voting.domain.voting import Voting


class VoteRepository(ABC):
    @abstractmethod
    def save(self, vote: Vote) -> None:
        pass

    @abstractmethod
    def get_vote_log(self, vote: Vote) -> None:
        pass

    @abstractmethod
    def get_all_votes(self, voting: Voting) -> None:
        pass