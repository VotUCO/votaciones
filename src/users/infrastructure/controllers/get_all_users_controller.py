import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from src.shared.infrastructure.is_admin_permission import IsAdminUser
from src.users.models import User

from src.users.application.user_finder import UserFinder
from src.users.infrastructure.builders.user_builder import UserBuilder
from src.users.infrastructure.mysql_user_repository import MySQLUserRepository
from src.users.infrastructure.serializers.user_serializer import UserSerializer


class FindAllUsersController(APIView):
    permission_classes = [IsAdminUser]
    http_method_names = ["get"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__user_builder = UserBuilder()
        self.__user_serializer = UserSerializer()
        self.__user_repository = MySQLUserRepository(self.__user_builder)
        self.__user_finder = UserFinder(self.__user_repository)

    def get(self, request: Request) -> Response:
        users = self.__user_finder.find_all()
        return Response(status=status.HTTP_200_OK, data=self.__user_serializer.serialize_all(users))