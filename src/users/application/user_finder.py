from typing import Any, List
from src.users.domain.user import User
from src.users.domain.user_repository import UserRepository


class UserFinder:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def find_by_user_and_pass(self, user: User) -> User | None:
        found_user = self.__user_repository.get_by_user_pass(user)
        return found_user

    def find_by_id(self, user: User) -> User:
        found_user = self.__user_repository.get_user_by_id(user)
        return found_user

    def find_by_email(self, user: User) -> Any:
        found_user = self.__user_repository.get_user_by_email(user)
        return found_user

    def find_all(self) -> List[User]:
        found_users = self.__user_repository.get_all()
        return found_users