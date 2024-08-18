import uuid
from rest_framework.test import APITestCase, APIClient
from datetime import datetime
from src.users.models import User
from faker import Faker
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from src.voting.domain.value_objects.status_enum import StatusEnum
from src.voting.domain.value_objects.voting_system_enum import VotingSystemEnum

class FindPrivateVotingControllerTest(APITestCase):
    def test_find_private_votings_on_list(self):
        faker = Faker()
        client = APIClient()
        email = faker.email()
        user = User.objects.create(id=faker.uuid4(),
                                   name=faker.word(),
                                   surname=faker.word(),
                                   email=email,
                                   password=faker.password(),
                                   gender=faker.random_element(["masculino", "femenino", "nobinario", "prefieronodecirlo", "otro"]),
                                   birth_date=faker.past_date(),
                                   rol="admin",
                                   date_joined=faker.date_time()
                                   )
        user.save()
        data={
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "email": email,
            "password": user.password,
            "gender": user.gender,
            "birthDate": str(datetime.strftime(datetime.now(), '%d-%m-%Y')),
            "rol": user.rol,
            "date_joined": user.date_joined
        }
        response=client.post(reverse("register-view"), data=data, format='json')
        token = RefreshToken.for_user(user)
        data = {
            "id":faker.uuid4(),
            "name":faker.word(),
            "state":StatusEnum.PUBLISHED.value,
            "winners":faker.random_int(),
            "voting_system":(faker.random_element(VotingSystemEnum)).value,
            "privacy":"True",
            "start_date":datetime.strftime(faker.past_datetime(), "%d/%m/%Y, %H:%M:%S"),
            "end_date":datetime.strftime(faker.future_datetime(), "%d/%m/%Y, %H:%M:%S"),
            "created_at":datetime.strftime(faker.date_time(), "%d/%m/%Y, %H:%M:%S"),
            "options":str([faker.word() for i in range (0,5)]),
            "authorized_user": f"['{user.email}']"
        }
        client.credentials(HTTP_AUTHORIZATION='Bearer '+str(token.access_token))
        response=client.post(reverse("voting-creation-controler"), data=data, format='json')
        response = client.get(reverse("get-private-votings"), data=data, format='json')
        for item in response.data:
            if item.get("id") == uuid.UUID(data.get("id")):
                assert True
                return 0
        assert False

    def test_find_private_votings_not_in_list(self):
        faker = Faker()
        user = User.objects.create(id=faker.uuid4(),
                                   name=faker.word(),
                                   surname=faker.word(),
                                   email='example@example.com',
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
            "privacy":"True",
            "start_date":datetime.strftime(faker.past_datetime(), "%d/%m/%Y, %H:%M:%S"),
            "end_date":datetime.strftime(faker.future_datetime(), "%d/%m/%Y, %H:%M:%S"),
            "created_at":datetime.strftime(faker.date_time(), "%d/%m/%Y, %H:%M:%S"),
            "options":str([faker.word() for i in range (0,5)]),
            "authorized_user": str([faker.word() for i in range(0,5)])
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer '+str(token.access_token))
        response=client.post(reverse("voting-creation-controler"), data=data, format='json')
        response = client.get(reverse("get-public-votings"), data=data, format='json')
        for item in response.data:
            if item.get("id") == uuid.UUID(data.get("id")):
                assert False
        assert True