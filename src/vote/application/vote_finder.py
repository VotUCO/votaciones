from typing import Any
from src.vote.domain.vote import Vote
from src.vote.domain.vote_repository import VoteRepository
from src.voting.domain.voting import Voting
from src.users.domain.user import User


class VoteFinder:
    def __init__(self, vote_repository: VoteRepository):
        self.__vote_repository = vote_repository

    def find_vote_log(self, vote: Vote) -> Vote | None:
        found_vote = self.__vote_repository.get_vote_log(vote)
        return found_vote
    
    def find_user_voted(self, user: User, voting: Voting) -> bool:
        user_vote = self.__vote_repository.user_voted(user, voting)
        if user_vote:
            return True
        else: 
            return False
        
    def find_user_authorized(self, user: User, voting: Voting) -> bool:
        user_authorized = self.__vote_repository.user_authorized(user, voting)
        if user_authorized:
            return True
        else:
            return False
