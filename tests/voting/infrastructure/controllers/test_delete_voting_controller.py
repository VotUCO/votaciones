from rest_framework.test import APITestCase, APIClient
from datetime import datetime
from src.users.models import User
from faker import Faker
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from src.voting.domain.value_objects.status_enum import StatusEnum
import random
from src.voting.domain.value_objects.voting_system_enum import VotingSystemEnum

class DeleteVotingControllerTest(APITestCase):
    def test_delete_voting_authenticate(self):
        faker = Faker()
        user = User.objects.create(id=faker.uuid4(),
                                   name=faker.word(),
                                   surname=faker.word(),
                                   email=faker.email(),
                                   password=faker.password(),
                                   gender=faker.random_element(["masculino", "femenino", "nobinario", "prefieronodecirlo", "otro"]),
                                   birth_date=faker.past_date(),
                                   rol="admin",
                                   date_joined=faker.date_time()
                                   )
        user.save()
        token = RefreshToken.for_user(user)
        data = {
            "id":faker.uuid4(),
            "name": faker.word(),
            "state":StatusEnum.DRAFT.value,
            "winners":random.randint(1, 4),
            "voting_system":(faker.random_element(VotingSystemEnum)).value,
            "privacy":"True",
            "start_date":datetime.strftime(faker.past_datetime(), "%d/%m/%Y, %H:%M:%S"),
            "end_date":datetime.strftime(faker.future_datetime(), "%d/%m/%Y, %H:%M:%S"),
            "voting_creator": user.id,
            "created_at":datetime.strftime(faker.date_time(), "%d/%m/%Y, %H:%M:%S"),
            "options":str([faker.word() for i in range (0,5)]),
            "authorized_user": str([faker.word() for i in range (0,5)]),
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer '+str(token.access_token))
        client.post(reverse("voting-creation-controler"), data=data, format='json')
        response = client.delete(reverse("voting-delete-view"), data=data, format='json')
        assert response.status_code == 200

    def test_delete_voting_not_being_owner(self):
        faker = Faker()
        user = User.objects.create(id=faker.uuid4(),
                                   name=faker.word(),
                                   surname=faker.word(),
                                   email=faker.email(),
                                   password=faker.password(),
                                   gender=faker.random_element(["masculino", "femenino", "nobinario", "prefieronodecirlo", "otro"]),
                                   birth_date=faker.past_date(),
                                   rol="admin",
                                   date_joined=faker.date_time()
                                   )
        user.save()
        token = RefreshToken.for_user(user)
        data = {
            "id":faker.uuid4(),
            "name": faker.word(),
            "state":StatusEnum.DRAFT.value,
            "winners":random.randint(1, 4),
            "voting_system":(faker.random_element(VotingSystemEnum)).value,
            "privacy":"True",
            "start_date":datetime.strftime(faker.past_datetime(), "%d/%m/%Y, %H:%M:%S"),
            "voting_creator": faker.uuid4(),
            "end_date":datetime.strftime(faker.future_datetime(), "%d/%m/%Y, %H:%M:%S"),
            "created_at":datetime.strftime(faker.date_time(), "%d/%m/%Y, %H:%M:%S"),
            "options":str([faker.word() for i in range (0,5)]),
            "authorized_user": str([faker.word() for i in range (0,5)]),
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer '+str(token.access_token))
        client.post(reverse("voting-creation-controler"), data=data, format='json')
        response = client.delete(reverse("voting-delete-view"), data=data, format='json')
        assert response.status_code == 403
