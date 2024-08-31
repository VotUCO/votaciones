import json
from typing import Dict, List

from src.voting.domain.voting import Voting
from src.voting.domain.voting_repository import VotingRepository
from src.voting.infrastructure.builders.voting_builder import VotingBuilder
from src.users.domain.user import User
import postgres as PostgresSQL
from src.votaciones.settings import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    VOTING_TABLE,
    VOTING_COLLECTION,
    AUTHORIZED_USERS_TABLE,
    OPTIONS_TABLE,
    USERS_TABLE,
    POSTGRES_DATABASE,
)
from src.voting.infrastructure.serializers.voting_serializer import VotingSerializer
from src.voting.infrastructure.serializers.option_serializer import OptionSerializer


class MySQLVotingRepository(VotingRepository):
    def __init__(self, voting_builder: VotingBuilder):
        self.__voting_builder = voting_builder
        self.__option_serializer = OptionSerializer()
        self.__voting_serializer = VotingSerializer()
        self.__client = PostgresSQL.Postgres(
            url=f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
        )

    def save(self, voting: Voting) -> Voting:
        self.__client.run(
            f"INSERT INTO {VOTING_COLLECTION}.{VOTING_TABLE} (id, name, state, winners, voting_system, privacy, start_date, end_date, created_at, voting_creator) VALUES ('{voting.id}', '{voting.name}', '{voting.state.value}', '{voting.winners}', '{voting.voting_system.value}', '{voting.privacy}', '{voting.start_date}', '{voting.end_date}', '{voting.created_at}', '{voting.voting_creator}')"
        )
        if voting.privacy == "True":
            for user in voting.authorized_user:
                self.__client.run(
                    f"INSERT INTO {VOTING_COLLECTION}.{AUTHORIZED_USERS_TABLE} (voting_id, user_email) VALUES ('{voting.id}', '{user}')"
                )
        for option in voting.options:
            self.__client.run(
                f"INSERT INTO {VOTING_COLLECTION}.{OPTIONS_TABLE} (option, voting_id) VALUES ('{option}', '{voting.id}')"
            )
        return voting

    def find_public_votings_active(self) -> List[Voting]:
        public_active_votings = self.__client.all(
            f"SELECT id, name, winners, voting_system, start_date, end_date FROM {VOTING_COLLECTION}.{VOTING_TABLE} WHERE start_date < CURRENT_TIMESTAMP AND end_date > CURRENT_TIMESTAMP AND privacy='False' AND state='published'"
        )
        public_active_voting_build = (
            self.__voting_serializer.for_user_record_all_serializer(
                public_active_votings
            )
        )
        public_active_voting_build_result = []
        for public_active_voting in public_active_voting_build:
            public_active_voting_build_result.append(
                self.__voting_builder.build(public_active_voting)
            )
        return public_active_voting_build_result

    def find_private_votings_active(self, user: User) -> List[Voting]:
        find_user_by_email = self.__client.one(
            f"SELECT email FROM {VOTING_COLLECTION}.{USERS_TABLE} WHERE id='{user.id}'"
        )
        find_voting_user_authorized = self.__client.all(
            f"SELECT voting_id FROM {VOTING_COLLECTION}.{AUTHORIZED_USERS_TABLE} WHERE user_email='{find_user_by_email}'"
        )
        voting_ids = []
        for voting_id in find_voting_user_authorized:
            voting_ids.append(str(voting_id))
        private_active_voting_result = []
        if len(voting_ids) != 0:
            private_active_votings = self.__client.all(
                f"SELECT id, name, winners, voting_system, start_date, end_date FROM {VOTING_COLLECTION}.{VOTING_TABLE} WHERE start_date < CURRENT_TIMESTAMP AND end_date > CURRENT_TIMESTAMP AND privacy='True' AND state='published' AND id=ANY(ARRAY{str(voting_ids)}::uuid[])"
            )
            private_active_voting_build = (
                self.__voting_serializer.for_user_record_all_serializer(
                    private_active_votings
                )
            )
            for private_active_voting in private_active_voting_build:
                private_active_voting_result.append(
                    self.__voting_builder.build(private_active_voting)
                )
        return private_active_voting_result

    def find_voting_by_user_active(self, user: User) -> List[Voting]:
        active_votings_by_user = self.__client.all(
            f"SELECT id, name, state, winners, voting_system, privacy, start_date, end_date, created_at, voting_creator FROM {VOTING_COLLECTION}.{VOTING_TABLE} WHERE start_date < CURRENT_TIMESTAMP AND end_date > CURRENT_TIMESTAMP AND state='published' AND voting_creator='{user.id}'"
        )
        active_votings_by_user_build = []
        for active_voting_by_user in active_votings_by_user:
            active_votings_by_user_build.append(
                self.__voting_builder.build_from_record(active_voting_by_user)
            )
        return active_votings_by_user_build
    
    def find_voting_by_user_draft(self, user: User) -> List[Voting]:
        draft_votings_by_user = self.__client.all(
            f"SELECT id, name, state, winners, voting_system, privacy, start_date, end_date, created_at, voting_creator FROM {VOTING_COLLECTION}.{VOTING_TABLE} WHERE end_date > CURRENT_TIMESTAMP AND state='draft' AND voting_creator='{user.id}'"
        )
        draft_votings_by_user_build = []
        for draft_voting_by_user in draft_votings_by_user:
            draft_votings_by_user_build.append(
                self.__voting_builder.build_from_record(draft_voting_by_user)
            )
        return draft_votings_by_user_build

    def find_voting_by_user_archived(self, user: User) -> List[Voting]:
        archived_votings_by_user = self.__client.all(
            f"SELECT id, name, state, winners, voting_system, privacy, start_date, end_date, created_at, voting_creator FROM {VOTING_COLLECTION}.{VOTING_TABLE} WHERE end_date < CURRENT_TIMESTAMP AND voting_creator='{user.id}'"
        )
        archived_votings_by_user_build = []
        for archived_voting_by_user in archived_votings_by_user:
            archived_votings_by_user_build.append(
                self.__voting_builder.build_from_record(archived_voting_by_user)
            )
        return archived_votings_by_user_build
    
    def publish_voting(self, voting: Voting) -> None:
        self.__client.run(
            f"UPDATE "
        )

    def find_voting_by_id(self, voting: Voting) -> Voting:
        votings_by_id = self.__client.one(
            f"SELECT * FROM {VOTING_COLLECTION}.{VOTING_TABLE} WHERE id='{voting.id}'::uuid"
        )
        if votings_by_id:
            return self.__voting_builder.build_from_record(votings_by_id)
        else:
            return None

    def update(self, voting: Voting) -> None:
        self.__client.run(
            f"UPDATE {VOTING_COLLECTION}.{VOTING_TABLE} SET name='{voting.name}', state='{voting.state.value}', voting_system='{voting.voting_system.value}', privacy='{voting.privacy}', start_date='{voting.start_date}', end_date='{voting.end_date}' WHERE id='{voting.id}'"
        )
        if voting.authorized_user != None:
            self.__client.run(
                f"DELETE FROM {VOTING_COLLECTION}.{AUTHORIZED_USERS_TABLE} WHERE voting_id='{voting.id}'"
            )
            for user in voting.authorized_user:
                self.__client.run(
                    f"INSERT INTO {VOTING_COLLECTION}.{AUTHORIZED_USERS_TABLE} (voting_id, user_email) VALUES ('{voting.id}', '{user}')"
                )
        if voting.options != None:
            self.__client.run(
                f"DELETE FROM {VOTING_COLLECTION}.{OPTIONS_TABLE} WHERE voting_id='{voting.id}'"
            )
            for option in voting.options:
                self.__client.run(
                    f"INSERT INTO {VOTING_COLLECTION}.{OPTIONS_TABLE} (option, voting_id) VALUES ('{option}', '{voting.id}')"
                )

    def delete(self, voting: Voting) -> None:
        self.__client.run(
            f"DELETE FROM {VOTING_COLLECTION}.{OPTIONS_TABLE} WHERE voting_id='{voting.id}'"
        )
        self.__client.run(
            f"DELETE FROM {VOTING_COLLECTION}.{AUTHORIZED_USERS_TABLE} WHERE voting_id='{voting.id}'"
        )
        self.__client.run(
            f"DELETE FROM {VOTING_COLLECTION}.{VOTING_TABLE} WHERE id='{voting.id}'"
        )

    def find_options_by_voting_id(self, voting: Voting) -> Dict:
        options = self.__client.all(
            f"SELECT option FROM {VOTING_COLLECTION}.{OPTIONS_TABLE} WHERE voting_id='{voting.id}'"
        )
        if options:
            return options
        else:
            return None
        
    def publish_vote(self, voting: Voting) -> None:
        self.__client.run(
            f"UPDATE {VOTING_COLLECTION}.{VOTING_TABLE} SET state='published', privacy='{voting.privacy}' WHERE id='{voting.id}'"
        )
        if voting.privacy == 'True':
            for user in voting.authorized_user:
                self.__client.run(
                    f"INSERT INTO {VOTING_COLLECTION}.{AUTHORIZED_USERS_TABLE} (voting_id, user_email) VALUES ('{voting.id}', '{user}')"
                )
