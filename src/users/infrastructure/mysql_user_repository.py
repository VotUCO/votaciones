import json
from typing import Any, List
from src.users.domain.user_repository import UserRepository
from src.users.infrastructure.builders.user_builder import UserBuilder
from src.users.domain.user import User
import postgres as PostgresSQL
from src.votaciones.settings import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    VOTING_COLLECTION,
    USERS_TABLE,
    POSTGRES_DATABASE,
    AUTHORIZED_USERS_TABLE
)
from src.voting.domain.voting import Voting


class MySQLUserRepository(UserRepository):
    def __init__(self, user_builder: UserBuilder):
        self.__user_builder = user_builder
        self.__client = PostgresSQL.Postgres(
            url=f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
        )

    def save(self, user: User) -> User:
        self.__client.run(
            f"""INSERT INTO {VOTING_COLLECTION}.{USERS_TABLE} (id, name, surname, email, password, gender, birth_date, rol, date_joined) VALUES ('{str(user.id)}', '{user.name}', '{user.surname}', '{user.email}', E'{user.password}', '{user.gender.value}', '{user.birthDate}', '{str(user.rol.value)}', CURRENT_TIMESTAMP)""",
            password=user.password,
        )
        return user

    def get_by_user_pass(self, user: User) -> Any:
        user_get = self.__client.one(
            f"SELECT id, name, surname, password, email, birth_date, gender, rol FROM {VOTING_COLLECTION}.{USERS_TABLE} WHERE email = '{user.email}' AND password = '{user.password}'"
        )
        if user_get:
            return self.__user_builder.build_from_record(user_get)
        else:
            return None

    def get_user_by_id(self, user: User) -> Any:
        user = self.__client.one(
            f"SELECT id, name, surname, email, birth_date, gender FROM {VOTING_COLLECTION}.{USERS_TABLE} WHERE id = '{user.id}'"
        )
        if user:
            return self.__user_builder.build_from_record_vote(user)
        else:
            return None

    def get_user_by_email(self, user: User) -> Any:
        found_user = self.__client.one(
            f"SELECT email, password FROM {VOTING_COLLECTION}.{USERS_TABLE} WHERE email='{user.email}'"
        )
        if found_user:
            return self.__user_builder.build_from_record_email_pass(found_user)
        else:
            return None
        
    def get_all(self) -> List[User]:
        found_users = self.__client.all(
            f"SELECT id, name, surname, email, gender, birth_date, rol FROM {VOTING_COLLECTION}.{USERS_TABLE}"
        )
        users = []
        for user in found_users:
            users.append(self.__user_builder.build_from_record_admin(user))
        return users

    def delete(self, user: User) -> None:
        self.__client.run(
            f"DELETE FROM {VOTING_COLLECTION}.{USERS_TABLE} WHERE id='{user.id}'"
        )
    
    def update(self, user: User) -> None:
        self.__client.run(
            f"UPDATE FROM {VOTING_COLLECTION}.{USERS_TABLE} SET name='{user.name}', surname='{user.surname}', email='{user.email}', password='{user.password}', gender='{user.gender.value}', "
        )

    def find_authorized_user(self, user: User, voting: Voting) -> bool:
        user = self.__client.one(
            f"SELECT * FROM {VOTING_COLLECTION}.{AUTHORIZED_USERS_TABLE} where voting_id='{voting.id}' and user_email='{user.email}'"
        )
        if user:
            True
        else:
            False

