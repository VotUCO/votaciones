import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from src.shared.infrastructure.is_admin_permission import IsAdminUser
from src.users.models import User

from src.users.infrastructure.builders.user_builder import UserBuilder
from src.users.infrastructure.mysql_user_repository import MySQLUserRepository
from src.users.application.user_deleter import UserDeleter


class DeleteUserController(APIView):
    permission_classes = [IsAdminUser]
    http_method_names = ["delete"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__user_builder = UserBuilder()
        self.__user_repository = MySQLUserRepository(self.__user_builder)
        self.__user_deleter = UserDeleter(self.__user_repository)

    def delete(self, request: Request) -> Response:
        if request.query_params["id"]:
            id = request.query_params["id"]
            user = self.__user_builder.build({"id": id})
            found_user = self.__user_deleter.delete(user)
            return Response(
                status=status.HTTP_200_OK,
                    data={"success": "Usuario {id} eliminado"},
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"error": "No se ha dado el id del usuario a modificar"}
            )
