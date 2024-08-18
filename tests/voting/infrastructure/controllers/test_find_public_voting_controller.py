import uuid
from rest_framework.test import APITestCase, APIClient
from datetime import datetime
from src.users.models import User
from faker import Faker
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from src.voting.domain.value_objects.status_enum import StatusEnum
from src.voting.domain.value_objects.voting_system_enum import VotingSystemEnum

class FindPublicVotingControllerTest(APITestCase):
    def test_find_public_votings(self):
        faker = Faker()
        user = User.objects.create(id=faker.uuid4(),
                                   name=faker.word(),
                                   surname=faker.word(),
                                   email=faker.email(),
                                   password=faker.password(),
                                   gender=faker.random_element(["masculino", "femenino", "nobinario", "other", "notsaid"]),
                                   birth_date=faker.past_date(),
                                   rol="admin",
                                   date_joined=faker.date_time()
                                   )
        user.save()
        token = RefreshToken.for_user(user)
        data = {
            "id":faker.uuid4(),
            "name":faker.word(),
            "state":StatusEnum.PUBLISHED.value,
            "winners":faker.random_int(),
            "voting_system":(faker.random_element(VotingSystemEnum)).value,
            "privacy":"False",
            "start_date":datetime.strftime(faker.past_datetime(), "%d/%m/%Y, %H:%M:%S"),
            "end_date":datetime.strftime(faker.future_datetime(), "%d/%m/%Y, %H:%M:%S"),
            "created_at":datetime.strftime(faker.date_time(), "%d/%m/%Y, %H:%M:%S"),
            "options":str([faker.word() for i in range (0,5)]),
            "authorized_user": ""
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer '+str(token.access_token))
        response=client.post(reverse("voting-creation-controler"), data=data, format='json')
        response = client.get(reverse("get-public-votings"), data=data, format='json')
        for item in response.data:
            if item.get("id") == uuid.UUID(data.get("id")):
                assert True
                return 0
        assert False
