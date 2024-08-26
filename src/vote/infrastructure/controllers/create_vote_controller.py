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
from src.vote.infrastructure.mongo_vote_repository import MongoVoteRepository
from src.vote.infrastructure.mysql_vote_repository import MySQLVoteRepository
from src.vote.infrastructure.serializers.vote_serializer import VoteSerializer
from src.voting.application.voting_finder import VotingFinder
from src.voting.infrastructure.mysql_voting_repository import MySQLVotingRepository
from src.voting.infrastructure.builders.voting_builder import VotingBuilder
from src.vote.application.vote_finder import VoteFinder
from src.users.infrastructure.builders.user_builder import UserBuilder

class CreateVoteController(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        self.__vote_builder = VoteBuilder()
        self.__voting_builder = VotingBuilder()
        self.__user_builder = UserBuilder()
        self.__voting_repository = MySQLVotingRepository(self.__voting_builder)
        self.__voting_finder = VotingFinder(self.__voting_repository)
        self.__vote_serializer = VoteSerializer()
        self.__mongo_vote_repository = MongoVoteRepository()
        self.__mysql_vote_repository = MySQLVoteRepository(self.__vote_builder)
        self.__vote_finder = VoteFinder(self.__mysql_vote_repository)
        self.__vote_log_creator = VoteCreator(self.__mysql_vote_repository)
        self.__vote_creator = VoteCreator(self.__mongo_vote_repository)

    @swagger_auto_schema(
        operation_description="An user can create a new vote",
        responses={200: VoteSerializer(), 401: "Unathorized"},
    )   
    def post(self, request: Request):
        if request.META.get("HTTP_AUTHORIZATION"):
            token = jwt.decode(
                request.META["HTTP_AUTHORIZATION"].split()[1],
                options={"verify_signature": False},
            )
            user_id = token["user_id"]
            vote = self.__vote_builder.build(json.loads(request.body))
            voting = self.__voting_finder.find_voting_by_id(self.__voting_builder.build({"id": vote.voting_id}))
            user = self.__user_builder.build({"id": user_id})
            if voting is None:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Votación no encontrada"})

            if self.__vote_finder.find_user_voted(user, voting):
                return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "El usuario ya ha votado"})
            if voting.privacy == "True":
                if self.__vote_finder.find_user_authorized(user, voting) == False:
                    return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "El usuario no está autorizado a votar"})
            vote.user_id = user_id
            self.__vote_log_creator.create(voting, vote)
            self.__vote_creator.create(vote)
            vote_serialized = self.__vote_serializer.serialize(vote)
            return Response(status=status.HTTP_200_OK, data=vote_serialized)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "El usuario no se ha identificado de manera válida"})