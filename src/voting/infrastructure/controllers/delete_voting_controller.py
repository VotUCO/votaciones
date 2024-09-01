import json
import jwt
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token

from src.voting.application.voting_deleter import VotingDeleter
from src.voting.infrastructure.builders.voting_builder import VotingBuilder
from src.voting.infrastructure.mysql_voting_repository import MySQLVotingRepository
from src.voting.application.voting_finder import VotingFinder

class DeleteVotingController(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["delete"]

    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        self.__voting_builder = VotingBuilder()
        self.__voting_repository = MySQLVotingRepository(self.__voting_builder)
        self.__voting_finder = VotingFinder(self.__voting_repository)
        self.__voting_deleter = VotingDeleter(
            self.__voting_repository
        )

    def delete(self, request: Request) -> Response:
        if request.META.get("HTTP_AUTHORIZATION"):
            token = jwt.decode(                
                request.META["HTTP_AUTHORIZATION"].split()[1],
                options={"verify_signature": False},
                )
            voting = self.__voting_finder.find_voting_by_id(self.__voting_builder.build({"id": request.query_params["id"]}))
            user_id = token["user_id"]
            if user_id == str(voting.voting_creator):
                update_status = self.__voting_deleter.delete(voting)
                if update_status == None:
                    return Response(
                        status=status.HTTP_200_OK,
                        data={"success": "Se ha borrado la votación"},
                    )
                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={"error": f"{str(update_status)}"},
                    )
            else:
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data={
                        "error": "No se puede eliminar una votación de la que no es creador"
                    },
                )
        else:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"error": "No se ha proporcionado un token de usuario válido"}
            )
