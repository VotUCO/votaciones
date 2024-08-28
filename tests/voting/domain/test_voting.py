from django.test import TestCase
from faker import Faker
from src.voting.domain.value_objects.status_enum import StatusEnum
from src.voting.domain.value_objects.voting_system_enum import VotingSystemEnum
from src.voting.domain.voting import Voting

class VotingTest(TestCase):
    def setUp(self):
        self.__faker = Faker()
        self.__voting = Voting(id=self.__faker.uuid4(),
                               name=self.__faker.domain_word(),
                               state=StatusEnum.DRAFT.value,
                               winners=self.__faker.random_int(min=0, max=4),
                               voting_system=self.__faker.random_choices(VotingSystemEnum),
                               privacy="True",
                               start_date=self.__faker.past_datetime(),
                               end_date=self.__faker.future_datetime(),
                               voting_creator=self.__faker.uuid4(),
                               created_at=self.__faker.date_time(),
                               options=self.__faker.get_words_list(),
                               authorized_user=self.__faker.get_words_list())
        
    def test_is_voting_active(self):
        active = self.__voting.is_voting_active()
        self.assertEqual(active, True)
    
    def test_is_voting_public(self):
        public = self.__voting.is_public()
        self.assertEqual(public, False)
    
    def test_is_voting_published(self):
        published = self.__voting.is_published()
        self.assertEqual(published, False)

    def test_is_voting_draft(self):
        draft = self.__voting.is_draft()
        self.assertEqual(draft, True)

    def add_option(self):
        self.__voting.add_option('Example')
        self.assertIn('Example', self.__voting.options)
                               

    