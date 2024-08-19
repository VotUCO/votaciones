from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from voting.api.serializers import UserVotingSerializer
from voting.models import Voting, AuthorizedUsers, Options
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class VotacionTest(APITestCase):

    """"This method execute before running each test"""
    def setUp(self):
        self.votation = Voting.objects.create(
           name = 'Elección Cafetería Rabanales',
           voting_system = 'Scoring',
           privacy = False,
           start_date = "2024-08-10T10:10:10",
           end_date= "2027-10-11T23:59:59",
           voting_creator = 'Jesús Escribano'
        )
        self.private_votation= Voting.objects.create(
           name = 'Elección Cafetería Rabanales',
           voting_system = 'Scoring',
           privacy = False,
           start_date = "2024-08-10T10:10:10",
           end_date= "2027-10-11T23:59:59",
           voting_creator = 'Jesús Escribano'
        )
        self.user = User.objects.create_superuser(username='test', first_name='test', last_name='test', email='test@gmail.com', password='Test1234')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_voting(self):
        url= reverse('voting-creation-view')
        data = {'name': self.votation.name, 
                'voting_system': self.votation.voting_system,
                'privacy': self.votation.privacy,
                'start_date': self.votation.start_date,
                'end_date': self.votation.end_date,
                'voting_creator': self.votation.voting_creator
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["voting_system"], data["voting_system"])
        self.assertEqual(response.data["start_date"], data["start_date"])
        self.assertEqual(response.data["end_date"], data["end_date"])

    def test_get_voting(self):
        self.votation.save()
        response = self.client.get(reverse('get-public-votings'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.votation.name)
        self.assertEqual(response.data[0]["voting_system"], self.votation.voting_system)
        self.assertEqual(response.data[0]["start_date"],  self.votation.start_date)
        self.assertEqual(response.data[0]["end_date"], self.votation.end_date)