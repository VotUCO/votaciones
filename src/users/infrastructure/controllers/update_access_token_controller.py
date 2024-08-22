import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from src.users.application.user_creator import UserCreator
from src.users.infrastructure.builders.user_builder import UserBuilder
from src.users.infrastructure.mysql_user_repository import MySQLUserRepository
from src.users.infrastructure.serializers.user_serializer import UserSerializer


class CreateUserController(APIView):
    authentication_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__user_builder = UserBuilder()
        self.__user_serializer = UserSerializer()
        self.__user_repository = MySQLUserRepository(self.__user_builder)
        self.__user_creator = UserCreator(self.__user_repository)

    def post(self, request: Request) -> Response:
        user = self.__user_builder.build(json.loads(request.body))
        user_created = self.__user_creator.create(user)
        return Response(
            status=status.HTTP_200_OK,
            data={"success": self.__user_serializer.serialize(user_created)},
        )
