from src.voting.domain.value_objects.options import Options
from django.test import TestCase
from faker import Faker

class TestOption(TestCase):
    def setUp(self):
        self.__faker = Faker()

    def test_create_option(self):
        option = Options(option_name=self.__faker.word(), voting_id=self.__faker.uuid4())
        self.assertIsInstance(option, Options)