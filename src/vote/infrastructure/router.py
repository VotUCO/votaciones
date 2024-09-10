from django.urls import path
from src.vote.infrastructure.controllers.create_vote_controller import CreateVoteController
from src.vote.infrastructure.controllers.get_vote_controller import GetVoteController

urlpatterns = [
    path("create", CreateVoteController.as_view(), name="vote-create-controler"),
    path("check", GetVoteController.as_view(), name="get-vote-controller")
]
