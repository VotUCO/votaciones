from rest_framework.test import APITestCase, APIClient
from datetime import datetime
from src.users.models import User
from faker import Faker
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from src.voting.domain.value_objects.status_enum import StatusEnum
from src.voting.domain.value_objects.voting_system_enum import VotingSystemEnum

class GetOptionsControllerTest(APITestCase):
    def test_get_options_authenticate(self):
        faker = Faker()
        user = User.objects.create(id=faker.uuid4(),
                                   name=faker.word(),
                                   surname=faker.word(),
                                   email=faker.email(),
                                   password=faker.password(),
                                   gender=faker.random_element(["masculino", "femenino", "nobinario", "other", "notsaid"]),
                                   birth_date=faker.past_date(),
                                   rol="user",
                                   date_joined=faker.date_time()
                                   )
        user.save()
        token = RefreshToken.for_user(user)
 

        voting_id = faker.uuid4()
        
        options = str([faker.word() for i in range(0,5)])
        data = {
            "id": voting_id,
            "name": faker.word(),
            "state": StatusEnum.DRAFT.value,
            "winners": faker.random_int(min=0, max=4),
            "voting_system": (faker.random_element(VotingSystemEnum)).value,
            "privacy": "False",
            "start_date": datetime.strftime(faker.past_datetime(), "%d/%m/%Y, %H:%M:%S"),
            "end_date": datetime.strftime(faker.future_datetime(), "%d/%m/%Y, %H:%M:%S"),
            "created_at": datetime.strftime(faker.date_time(), "%d/%m/%Y, %H:%M:%S"),
            "options": options,
            "authorized_user": str([faker.word() for i in range(0,5)])
        }
        
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token.access_token))
        
        # Usamos el voting_id en la URL
        response = client.get(f"votuco/api/v1/voting/options?id={voting_id}", format='json')
        
        assert response.status_code == 200