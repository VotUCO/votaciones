import json
from typing import Any
from src.vote.infrastructure.builders.vote_builder import VoteBuilder
from src.vote.domain.vote_repository import VoteRepository
from src.vote.domain.vote import Vote
from src.users.domain.user import User
import postgres as PostgresSQL
from src.votaciones.settings import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    AUTHORIZED_USERS_TABLE,
    VOTING_COLLECTION,
    VOTE_TABLE,
    POSTGRES_DATABASE,
)
from src.voting.domain.voting import Voting



class MySQLVoteRepository(VoteRepository):
    def __init__(self, vote_builder: VoteBuilder):
        self.__vote_builder = vote_builder
        self.__client = PostgresSQL.Postgres(
            url=f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
        )

    def save(self, vote: Vote) -> None:
        self.__client.run(
            f"INSERT INTO {VOTING_COLLECTION}.{VOTE_TABLE} (voteToken, voteDateTime, votingId, userId, hasVoted) VALUES ('{vote.id}', '{vote.datetime}', '{vote.voting_id}', '{vote.user_id}', True)" 
        )

    def user_authorized(self, user: User, voting: Voting) -> bool:
        user = self.__client.one(
            f"SELECT * FROM {VOTING_COLLECTION}.{AUTHORIZED_USERS_TABLE} WHERE email='{user.email}'"
        )
        authorized = self.__client.one(
            f"SELECT * FROM {VOTING_COLLECTION}.{AUTHORIZED_USERS_TABLE} WHERE user_email='{user.email}' AND voting_id='{voting.id}'"
        ) 
        if authorized: 
            return True
        else:
            return False
        
    def user_voted(self, user: User, voting: Voting) -> bool:
        voted = self.__client.one(
            f"SELECT * FROM {VOTING_COLLECTION}.{VOTE_TABLE} WHERE votingid='{voting.id}' and userid='{user.id}'"
        )
        if voted:
            return True
        else:
            return False
    
    def get_vote_log(self, vote: Vote) -> None | Vote:
        vote = self.__client.one(
            f"SELECT * FROM {VOTING_COLLECTION}.{VOTE_TABLE} where voteToken='{vote.id}'"
        )
        if vote:
            return self.__vote_builder.build_from_record(vote)
        else:
            return None 
        
    def get_all_votes(self, voting: Voting) -> None:
        pass