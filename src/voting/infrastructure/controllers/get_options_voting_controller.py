import json
import random
import jwt
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from docs.create_voting_parameters import (
    name,
    state,
    voting_system,
    privacy,
    start_date,
    end_date,
)
from src.voting.infrastructure.serializers.voting_serializer import VotingSerializer
from src.voting.application.voting_creator import VotingCreator
from src.voting.infrastructure.builders.voting_builder import VotingBuilder
from src.voting.infrastructure.mysql_voting_repository import MySQLVotingRepository
from src.voting.application.voting_finder import VotingFinder


class GetOptionsVotingController(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        self.__voting_builder = VotingBuilder()
        self.__voting_repository = MySQLVotingRepository(self.__voting_builder)
        self.__voting_finder = VotingFinder(self.__voting_repository)

    def get(self, request: Request) -> Response:
        voting_id = request.query_params.get("id")
        options = self.__voting_finder.find_options_by_voting_id(
            self.__voting_builder.build({"id": voting_id})
        )
        if options:
            return Response(status=status.HTTP_200_OK, data=options)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=[{"error": "No se ha encontrado el id de votación proporcionado"}],
            )
