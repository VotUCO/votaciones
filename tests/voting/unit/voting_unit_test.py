from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from voting.models import Voting, AuthorizedUsers, Options

class VotacionTest(APITestCase):
    def setUp(self):
        self.votaction = Voting.objects.create(
           name = 'Elección Cafetería Rabanales',
           voting_system = 'Scoring',
           privacy = False,
           start_date = "2024-08-10 10:10:10",
           voting_creator = 'Jesús Escribano'
        )
        self.url= reverse('voting-view', kwargs={'name': self.votaction.name, 
                                                 'voting_system': self.votaction.voting_system,
                                                 'privacy': self.votaction.privacy,
                                                 'start_date': self.votaction.start_date,
                                                 'voting_creator': self.votaction.voting_creator})

    def test_obtener_votacion(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.votaction.name)