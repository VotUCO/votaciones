from django.test import TestCase
from faker import Faker
from src.voting.domain.value_objects.authorized_users import AuthorizedUser

class AuthorizedUserTest(TestCase):
    def setUp(self):
        self.__faker = Faker()

    def test_create_authorized_user(self):
        authorized_user = AuthorizedUser(user_id=self.__faker.uuid4, voting_id=self.__faker.uuid4)
        self.assertIsInstance(authorized_user, AuthorizedUser)