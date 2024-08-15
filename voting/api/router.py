from django.urls import path, include
from voting.api.router import router_voting
from voting.api.views import VotingAPIView
from voting.api.private_vote_views import PrivateVotingAPIView
from voting.api.public_vote_views import PublicVotingAPIView

router_voting = [
    path('/create', VotingAPIView.as_view()),
    path('/private', PrivateVotingAPIView.as_view()),
    path('/public', PublicVotingAPIView.as_view())
]