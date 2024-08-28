from abc import ABC, abstractmethod
from typing import Dict, List


from src.voting.domain.voting import Voting
from src.users.domain.user import User


class VotingRepository(ABC):
    @abstractmethod
    def save(self, voting: Voting) -> Voting:
        pass

    @abstractmethod
    def find_public_votings_active(self) -> List[Voting]:
        pass

    @abstractmethod
    def find_private_votings_active(self, user: User) -> List[Voting]:
        pass

    @abstractmethod
    def find_voting_by_user_active(self, user: User) -> List[Voting]:
        pass

    @abstractmethod
    def find_voting_by_user_archived(self, user: User) -> List[Voting]:
        pass

    @abstractmethod
    def find_voting_by_id(self, voting: Voting) -> Voting:
        pass

    @abstractmethod
    def update(self, voting: Voting) -> None:
        pass

    @abstractmethod
    def delete(self, voting: Voting) -> None:
        pass

    @abstractmethod
    def find_options_by_voting_id(self, voting: Voting) -> Dict:
        pass
