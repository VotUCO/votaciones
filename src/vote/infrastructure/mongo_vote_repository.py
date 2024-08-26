from pymongo import MongoClient
from src.vote.domain.vote_repository import VoteRepository
from src.vote.domain.vote import Vote
from src.votaciones.settings import (
    MONGO_HOST,
    MONGO_PASSWORD,
    MONGO_USER,
    MONGO_DATABASE,
    MONGO_PORT
)
from urllib.parse import quote_plus

class MongoVoteRepository(VoteRepository):
    def __init__(self):
        self.__client = MongoClient(f"mongodb://{quote_plus(MONGO_USER)}:{quote_plus(MONGO_PASSWORD)}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE}")
        self.__client = self.__client["voting"]

    def save(self, vote: Vote) -> None:
        vote_payload = {
            "vote": vote.vote,
            "datetime": vote.datetime,
        }
        voting_collection = self.__client[str(vote.voting_id)]
        voting_collection.insert_one(vote_payload)

    def get_vote_log(self, vote: Vote) -> None:
        pass