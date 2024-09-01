import json
import jwt
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from src.shared.infrastructure.is_admin_permission import IsAdminUser
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


class CreateVotingController(APIView):
    permission_classes = [IsAdminUser]
    http_method_names = ["post"]

    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        self.__voting_serializer = VotingSerializer()
        self.__voting_builder = VotingBuilder()
        self.__voting_repository = MySQLVotingRepository(self.__voting_builder)
        self.__voting_creator = VotingCreator(self.__voting_repository)

    @swagger_auto_schema(
        operation_description="An admin user can create a new voting proccess",
        responses={200: VotingSerializer(), 401: "Unathorized"},
        manual_parameters=[name, state, voting_system, privacy, start_date, end_date],
    )
    def post(self, request: Request) -> Response:
        if request.META.get("HTTP_AUTHORIZATION"):
            token = jwt.decode(
                request.META["HTTP_AUTHORIZATION"].split()[1],
                options={"verify_signature": False},
            )
            user_id = token["user_id"]
            voting = self.__voting_builder.build(json.loads(request.body))
            voting.voting_creator = user_id
            self.__voting_creator.create(voting)
            voting_serialized = self.__voting_serializer.serialize(voting)
            return Response(status=status.HTTP_200_OK, data=voting_serialized)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "El usuario no se ha identificado de manera válida"})
