import random
from typing import Any, Dict, List

from src.voting.domain.voting import Voting
from src.voting.domain.voting_repository import VotingRepository


class VotingFinder:
    def __init__(self, voting_repository: VotingRepository) -> None:
        self.__voting_repository = voting_repository

    def find_public_votings_active(self) -> List[Voting]:
        return self.__voting_repository.find_public_votings_active()

    def find_private_votings_active(self, user) -> List[Voting]:
        return self.__voting_repository.find_private_votings_active(user=user)

    def find_voting_by_user_active(self, user) -> List[Voting]:
        return self.__voting_repository.find_voting_by_user_active(user=user)

    def find_voting_by_user_archived(self, user) -> List[Voting]:
        return self.__voting_repository.find_voting_by_user_archived(user=user)
    
    def find_voting_by_user_draft(self, user) -> List[Voting]:
        return self.__voting_repository.find_voting_by_user_draft(user=user)

    def find_voting_by_id(self, voting: Voting) -> Voting:
        return self.__voting_repository.find_voting_by_id(voting=voting)

    def find_options_by_voting_id(self, voting: Voting) -> Any:
        options = self.__voting_repository.find_options_by_voting_id(voting=voting)
        if options:
            return {
                "options": random.sample(
                options, len(options)
            )
            } 
        else:
            return None
