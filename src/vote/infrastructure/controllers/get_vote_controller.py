import json
import jwt
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from src.vote.application.vote_creator import VoteCreator
from src.vote.infrastructure.builders.vote_builder import VoteBuilder
from src.vote.infrastructure.mysql_vote_repository import MySQLVoteRepository
from src.vote.infrastructure.serializers.vote_serializer import VoteSerializer
from src.voting.application.voting_finder import VotingFinder
from src.voting.infrastructure.mysql_voting_repository import MySQLVotingRepository
from src.voting.infrastructure.builders.voting_builder import VotingBuilder
from src.vote.application.vote_finder import VoteFinder
from src.users.infrastructure.builders.user_builder import UserBuilder
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from jinja2 import Template
from django.templatetags.static import static
from src.votaciones.settings import EMAIL_HOST_USER
from src.users.application.user_finder import UserFinder
from src.users.infrastructure.mysql_user_repository import MySQLUserRepository


class GetVoteController(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        self.__vote_builder = VoteBuilder()
        self.__vote_serializer = VoteSerializer()
        self.__mysql_vote_repository = MySQLVoteRepository(self.__vote_builder)
        self.__vote_finder = VoteFinder(self.__mysql_vote_repository)
        self.__voting_builder = VotingBuilder()
        self.__mysql_voting_repository = MySQLVotingRepository(self.__voting_builder)
        self.__voting_finder= VotingFinder(self.__mysql_voting_repository)
        self.__user_builder= UserBuilder()
        self.__user_repository = MySQLUserRepository(self.__user_builder)
        self.__user_finder = UserFinder(self.__user_repository)

    @swagger_auto_schema(
        operation_description="An user can create a new vote",
        responses={200: VoteSerializer(), 401: "Unathorized"},
    )   
    def get(self, request: Request):
        vote = self.__vote_builder.build({"id": request.query_params["id"]})
        vote = self.__vote_finder.find_vote_log(vote)
        voting = self.__voting_finder.find_voting_by_id(self.__voting_builder.build({"id": vote.voting_id}))
        user = self.__user_finder.find_by_id(self.__user_builder.build({"id": vote.user_id}))
        if vote is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Voto no encontrado"})
        voting = self.__voting_finder.find_voting_by_id(self.__voting_builder.build({"id": vote.voting_id}))
        user = self.__user_finder.find_by_id(self.__user_builder.build({"id": vote.user_id}))
        return Response(status=status.HTTP_200_OK, data=self.__vote_serializer.serialize_checker(vote, voting, user))