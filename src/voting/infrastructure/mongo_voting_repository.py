from pymongo import MongoClient
from src.voting.domain.voting_repository import VotingRepository
from vote.domain.vote import Vote
from src.votaciones.settings import (
    MONGO_HOST,
    MONGO_PASSWORD,
    MONGO_USER,
    MONGO_DATABASE,
)

class MongoVoteRepository(VotingRepository):
    def __init__(self):
        self.__client = MongoClient(f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DATABASE}")

    def save(self, vote: Vote) -> None:
        vote_payload = {
            "vote": vote.vote,
            "datetime": vote.datetime,
        }
        voting_collection = self.__client[vote.id]
        voting_collection.insert_one(vote_payload)