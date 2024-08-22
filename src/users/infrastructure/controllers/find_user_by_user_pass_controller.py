import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from src.users.models import User

from src.users.application.user_finder import UserFinder
from src.users.infrastructure.builders.user_builder import UserBuilder
from src.users.infrastructure.mysql_user_repository import MySQLUserRepository
from src.users.infrastructure.serializers.user_serializer import UserSerializer


class FindUserByUserPasswordController(APIView):
    http_method_names = ["post"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__user_builder = UserBuilder()
        self.__user_serializer = UserSerializer()
        self.__user_repository = MySQLUserRepository(self.__user_builder)
        self.__user_finder = UserFinder(self.__user_repository)

    def post(self, request: Request) -> Response:
        user = self.__user_builder.build(json.loads(request.body))
        found_user = self.__user_finder.find_by_user_and_pass(user)
        if found_user:
            found_user = User.objects.get(id=found_user.id)
            tokens = RefreshToken.for_user(found_user)
            refresh_token, access_token = str(tokens), str(tokens.access_token)
            return Response(
                status=status.HTTP_200_OK,
                data={"refresh": refresh_token, "access": access_token, "rol": found_user.rol, "nombre": found_user.name},
            )
        else:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"error": "Usuario o contraseña incorrectos"},
            )
