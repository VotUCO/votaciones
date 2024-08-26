from src.vote.domain.vote_repository import VoteRepository
from src.vote.domain.vote import Vote
from src.voting.domain.voting import Voting

class VoteCreator:
    def __init__(self, vote_repository: VoteRepository):
        self.__vote_repository = vote_repository

    def create(self, voting: Voting, vote: Vote) -> None:
        self.__vote_repository.save(vote)
