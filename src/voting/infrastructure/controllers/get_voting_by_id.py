from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt

from src.shared.infrastructure.is_admin_permission import IsAdminUser
from src.users.infrastructure.builders.user_builder import UserBuilder
from src.voting.application.voting_finder import VotingFinder
from src.voting.infrastructure.builders.voting_builder import VotingBuilder
from src.voting.infrastructure.mysql_voting_repository import MySQLVotingRepository
from src.voting.infrastructure.serializers.voting_serializer import VotingSerializer


class GetVotingByIdController(APIView):
    permission_classes = [IsAdminUser]
    http_method_names = ["get"]

    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        self.__voting_serializer = VotingSerializer()
        self.__voting_builder = VotingBuilder()
        self.__user_builder = UserBuilder()
        self.__voting_repository = MySQLVotingRepository(self.__voting_builder)
        self.__voting_finder = VotingFinder(self.__voting_repository)

    def get(self, request):
        token = jwt.decode(
            request.META["HTTP_AUTHORIZATION"].split()[1],
            options={"verify_signature": False},
        )
        user_id = token["user_id"]
        vote = self.__voting_builder.build({"id": request.query_params.get("id")})
        voting = self.__voting_finder.find_voting_by_id(vote)
        if str(voting.voting_creator) == user_id:
            return Response(
                status=status.HTTP_200_OK,
                data=self.__voting_serializer.for_user_serializer_modify(voting),
            )
        else:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"error": "No se puede consultar una votación de la que no se es creador"}
            )