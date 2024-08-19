from django.urls import path
from voting.api.views import VotingAPIView
from voting.api.private_vote_views import PrivateVotingAPIView
from voting.api.public_vote_views import PublicVotingAPIView

urlpatterns = [
    path('create', VotingAPIView.as_view(), name='voting-creation-view'),
    path('private', PrivateVotingAPIView.as_view(), name='get-private-votings'),
    path('public', PublicVotingAPIView.as_view(), name='get-public-votings')
]