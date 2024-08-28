from typing import List

from src.voting.domain.value_objects.status_enum import StatusEnum
from src.voting.domain.voting import Voting
from src.voting.domain.voting_repository import VotingRepository


class VotingDeleter:
    def __init__(self, voting_repository: VotingRepository) -> None:
        self.__voting_repository = voting_repository

    def delete(self, voting: Voting) -> None:
        if voting.state == StatusEnum.PUBLISHED.value:
            return TypeError("No se puede eliminar una votación ya publicada")
        return self.__voting_repository.delete(voting)
