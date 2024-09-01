import json
import jwt
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from src.voting.application.voting_updater import VotingUpdater
from src.voting.infrastructure.builders.voting_builder import VotingBuilder
from src.voting.infrastructure.mysql_voting_repository import MySQLVotingRepository
from src.voting.infrastructure.serializers.voting_serializer import VotingSerializer
from src.voting.application.voting_finder import VotingFinder

class UpdateVotingController(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["put"]

    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        self.__voting_serializer = VotingSerializer()
        self.__voting_builder = VotingBuilder()
        self.__voting_repository = MySQLVotingRepository(self.__voting_builder)
        self.__voting_finder = VotingFinder(self.__voting_repository)
        self.__voting_updater = VotingUpdater(
            self.__voting_repository, self.__voting_builder
        )

    def put(self, request: Request) -> Response:
        token = jwt.decode(request.META["HTTP_AUTHORIZATION"].split()[1],
            options={"verify_signature": False},)
        user_id = token["user_id"]
        voting_info = json.loads(request.body.decode('utf-8'))
        voting = self.__voting_builder.build({"id": voting_info.get("id")})
        voting = self.__voting_finder.find_voting_by_id(voting)
        if user_id == str(voting.voting_creator):
            voting = self.__voting_builder.build(voting_info)
            update_status = self.__voting_updater.update(voting)
            if update_status == None:
                return Response(
                    status=status.HTTP_200_OK,
                    data={"success": "Se ha modificado la votación"},
                )
            else:
                return Response(
                    status=status.HTTP_304_NOT_MODIFIED,
                    data={"error": f"{str(update_status)}"},
                )
        else:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    "error": "No se puede modificar una votación de la que no es creador"
                },
            )
