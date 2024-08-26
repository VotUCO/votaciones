from django.urls import path
from src.vote.infrastructure.controllers.create_vote_controller import CreateVoteController

urlpatterns = [
    path("create", CreateVoteController.as_view(), name="vote-create-controler"),
]
