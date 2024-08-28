from src.voting.domain.value_objects.status_enum import StatusEnum
from src.voting.domain.voting import Voting
from src.voting.domain.voting_repository import VotingRepository
from src.voting.infrastructure.builders.voting_builder import VotingBuilder
from apscheduler.schedulers.background import BackgroundScheduler
from src.voting.infrastructure.schedulers.generate_votation_report_scheduler import generate_votacion_pdf

class VotingUpdater:
    def __init__(
        self, voting_repository: VotingRepository, voting_builder: VotingBuilder
    ) -> None:
        self.__voting_repository = voting_repository
        self.__voting_builder = voting_builder

    def update(self, new_voting: Voting):
        old_voting = self.__voting_repository.find_voting_by_id(new_voting)
        if old_voting.state == StatusEnum.PUBLISHED.value:
            return TypeError("No se puede modificar una votación ya publicada")
        if old_voting.options == new_voting.options:
            new_voting.options = None
        if old_voting.authorized_user == new_voting.authorized_user:
            new_voting.authorized_user = None
        voting_to_update = self.__voting_builder.build_new_one(old_voting, new_voting)
        self.__voting_repository.update(voting_to_update)
    
    def publish(self, voting: Voting):
        self.__voting_repository.publish_vote(voting)
        scheduler = BackgroundScheduler()
        scheduler.add_job(generate_votacion_pdf, 'date', run_date=voting.end_date, args=[voting.id])
        scheduler.start()