from rest_framework.request import Request
from rest_framework.views import APIView
from src.votaciones.settings import BACK_URL, FRONT_REGISTER_URL, FRONT_URL, UCO_CLIENT_ID, UCO_SECRET_ID, UCO_AUTHORIZATION_URL, UCO_TOKEN_URL, UCO_USER_INFO
from rest_framework_simplejwt.tokens import RefreshToken
from authlib.integrations.django_client import OAuth
from src.users.infrastructure.builders.user_builder import UserBuilder
from src.users.infrastructure.mysql_user_repository import MySQLUserRepository
from src.users.models import User
from django.shortcuts import redirect

class UCOLoginCallbackController(APIView):
    http_method_names = ["get"]

    def __init__(self):
        self.__user_builder = UserBuilder()
        self.__user_repository = MySQLUserRepository(self.__user_builder)
        self.__oauth = OAuth()
        self.__oauth.register(
            name='uco',
            client_id=UCO_CLIENT_ID,
            client_secret=UCO_SECRET_ID,
            authorize_url=UCO_AUTHORIZATION_URL,
            token_url=UCO_TOKEN_URL,
            client_kwargs={'scope': 'email'},
        )
    def get(self, request: Request, *args, **kwargs):
        token = self.__oauth.provider.authorize_access_token(request)

        userinfo = self.__oauth.provider.get(UCO_USER_INFO).json()

        if userinfo:
            user = self.__user_repository.get_user_by_email(
                user=self.__user_builder.build(userinfo)
            )
            if user:
                found_user = User.objects.get(email=user.email)
                tokens = RefreshToken.for_user(found_user)
                refresh_token, access_token = str(tokens), str(tokens.access_token)
                return redirect(f'{FRONT_URL}/login/oauth?access_token={access_token}&refresh_token={refresh_token}&rol={found_user.rol}&name={found_user.name}')
            else:
                return redirect(f'{FRONT_REGISTER_URL}?email={userinfo["email"]}')
