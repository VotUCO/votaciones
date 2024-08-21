from abc import ABC, abstractmethod
from typing import Any, List

from src.users.domain.user import User
from src.voting.domain.voting import Voting


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_user_pass(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, user: User) -> Any:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        pass

    @abstractmethod
    def find_authorized_user(self, user: User, voting: Voting) -> bool:
        pass
