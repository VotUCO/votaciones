from src.voting.domain.voting import Voting
from src.voting.domain.voting_repository import VotingRepository
from datetime import datetime

from src.voting.infrastructure.schedulers.generate_votation_report_scheduler import generate_votacion_pdf

class VotingCreator:
    def __init__(self, voting_repository: VotingRepository) -> None:
        self.__voting_repository = voting_repository

    def create(self, voting: Voting) -> None:
        self.__voting_repository.save(voting)