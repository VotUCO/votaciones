from typing import List
from src.voting.infrastructure.mysql_voting_repository import MySQLVotingRepository
from src.voting.infrastructure.builders.voting_builder import VotingBuilder
from django.test import TestCase
from faker import Faker

from src.voting.domain.value_objects.status_enum import StatusEnum
from src.voting.domain.value_objects.voting_system_enum import VotingSystemEnum
from src.voting.domain.voting import Voting
from src.users.infrastructure.builders.user_builder import UserBuilder

class MySQLVotingRepositoryTest(TestCase):
    def setUp(self):
        self.__voting_builder = VotingBuilder()
        self.__repository = MySQLVotingRepository(self.__voting_builder)
        self.__user_builder = UserBuilder()
        self.__faker = Faker()
        self.__id = self.__faker.uuid4()

    def test_create_voting(self):
        voting = Voting(id=self.__id, 
                            name=self.__faker.word(),
                            state=StatusEnum.PUBLISHED,
                            winners=self.__faker.random_int(0,3),
                            voting_system=VotingSystemEnum.SCORING,
                            privacy=self.__faker.random_element(["True", "False"]),
                            start_date=self.__faker.past_datetime(),
                            end_date=self.__faker.future_datetime(),
                            voting_creator=self.__faker.uuid4(),
                            created_at=self.__faker.date_time(),
                            options=self.__faker.get_words_list(),
                            authorized_user=self.__faker.get_words_list()
                        )
        result_voting = self.__repository.save(voting=voting)
        self.assertEqual(voting, result_voting)

    def test_find_public_votings_active(self):
        votings = self.__repository.find_public_votings_active()
        self.assertIsInstance(votings, List)
        for voting in votings:
            self.assertIsInstance(voting, Voting)

    def test_find_private_votings_active(self):
        votings = self.__repository.find_private_votings_active(self.__user_builder.build({"id": self.__faker.uuid4()}))
        self.assertIsInstance(votings, List)
        for voting in votings:
            self.assertIsInstance(voting, Voting)

    def test_find_voting_by_user_active(self):
        votings = self.__repository.find_voting_by_user_active(self.__user_builder.build({"id": self.__faker.uuid4()}))
        self.assertIsInstance(votings, List)
        for voting in votings:
            self.assertIsInstance(voting, Voting)

    def test_find_voting_by_user_archived(self):
        votings = self.__repository.find_voting_by_user_archived(self.__user_builder.build({"id": self.__faker.uuid4()}))
        self.assertIsInstance(votings, List)
        for voting in votings:
            self.assertIsInstance(voting, Voting)

    def test_find_by_id(self):
        voting = Voting(id=self.__id, 
                        name=self.__faker.word(),
                        state=StatusEnum.PUBLISHED,
                        winners=self.__faker.random_int(0,3),
                        voting_system=VotingSystemEnum.SCORING,
                        privacy=self.__faker.random_element(["True", "False"]),
                        start_date=self.__faker.past_datetime(),
                        end_date=self.__faker.future_datetime(),
                        voting_creator=self.__faker.uuid4(),
                        created_at=self.__faker.date_time(),
                        options=self.__faker.get_words_list(),
                        authorized_user=self.__faker.get_words_list()
                        )
        self.__repository.save(voting=voting)
        voting = self.__voting_builder.build({"id": str(self.__id)})
        voting = self.__repository.find_voting_by_id(voting)
        self.assertEqual(str(voting.id), self.__id)

    def test_update_voting(self):
        voting = Voting(id=self.__id, 
                        name=self.__faker.word(),
                        state=StatusEnum.DRAFT,
                        winners=self.__faker.random_int(0,3),
                        voting_system=VotingSystemEnum.SCORING,
                        privacy=self.__faker.random_element(["True", "False"]),
                        start_date=self.__faker.past_datetime(),
                        end_date=self.__faker.future_datetime(),
                        voting_creator=self.__faker.uuid4(),
                        created_at=self.__faker.date_time(),
                        options=self.__faker.get_words_list(),
                        authorized_user=self.__faker.get_words_list()
                        )
        self.__repository.save(voting=voting)
        nombre_antiguo = voting.name
        voting.name= self.__faker.word()
        self.__repository.update(voting=voting)
        new_voting = self.__repository.find_voting_by_id(voting=voting)
        self.assertNotEqual(new_voting.name, nombre_antiguo)

    def test_delete_voting(self):
        voting = Voting(id=self.__id, 
                        name=self.__faker.word(),
                        state=StatusEnum.DRAFT,
                        winners=self.__faker.random_int(0,3),
                        voting_system=VotingSystemEnum.SCORING,
                        privacy=self.__faker.random_element(["True", "False"]),
                        start_date=self.__faker.past_datetime(),
                        end_date=self.__faker.future_datetime(),
                        voting_creator=self.__faker.uuid4(),
                        created_at=self.__faker.date_time(),
                        options=self.__faker.get_words_list(),
                        authorized_user=self.__faker.get_words_list()
                        )
        self.__repository.delete(voting=voting)
        no_voting = self.__repository.find_voting_by_id(voting)
        self.assertEqual(no_voting, None)