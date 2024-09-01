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


class PublishVotingController(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        self.__voting_serializer = VotingSerializer()
        self.__voting_builder = VotingBuilder()
        self.__voting_repository = MySQLVotingRepository(self.__voting_builder)
        self.__voting_finder = VotingFinder(
            self.__voting_repository
        )
        self.__voting_updater = VotingUpdater(
            self.__voting_repository, self.__voting_builder
        )

    def post(self, request: Request) -> Response:
        token = jwt.decode(request.META["HTTP_AUTHORIZATION"].split()[1],
            options={"verify_signature": False},)
        user_id = token["user_id"]
        voting = self.__voting_builder.build({"id": request.data.get("id")})
        found_voting = self.__voting_finder.find_voting_by_id(voting)
        print(found_voting)
        if user_id ==  str(found_voting.voting_creator):
            found_voting.privacy = "True" if request.data.get("privacy") == 'true' else "False"
            found_voting.authorized_user = eval(request.data.get("authorized_users"))
            self.__voting_updater.publish(found_voting)
            return Response(
                status=status.HTTP_200_OK,
                data={"success": f"Votación {voting.id} publicada"},
            )
        else:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    "error": "No se puede modificar una votación de la que no es creador"
                },
            )
