from src.users.domain.user import User
from src.users.domain.user_repository import UserRepository


class UserCreator:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def create(self, user: User) -> User:
        user = self.__user_repository.save(user)
        return user
