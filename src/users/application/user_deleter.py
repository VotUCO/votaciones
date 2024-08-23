from src.users.domain.user import User
from src.users.domain.user_repository import UserRepository


class UserDeleter:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def delete(self, user: User) -> User:
        user = self.__user_repository.delete(user)
        return user
