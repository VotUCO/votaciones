from abc import ABC, abstractmethod
from typing import Any, Dict

from src.voting.domain.voting import Voting


class Builder(ABC):
    @abstractmethod
    def build(self, json: Dict) -> Any:
        pass

    @abstractmethod
    def build_new_one(self, old_vote: Voting, new_vote: Voting) -> Any:
        pass
