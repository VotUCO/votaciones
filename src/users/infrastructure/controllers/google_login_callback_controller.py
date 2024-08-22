import google_auth_oauthlib
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from src.votaciones.settings import BACK_URL, FRONT_REGISTER_URL, FRONT_URL
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect

from src.users.application.user_finder import UserFinder
from src.users.infrastructure.builders.user_builder import UserBuilder
from src.users.infrastructure.mysql_user_repository import MySQLUserRepository
from src.users.models import User


class GoogleLoginCallbackController(APIView):
    http_method_names = ["get"]

    def __init__(self):
        self.__user_builder = UserBuilder()
        self.__user_repository = MySQLUserRepository(self.__user_builder)
        self.__user_finder = UserFinder(self.__user_repository)

    def get(self, request: Request, *args, **kwargs):
        state = request.session["state"]
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            "client_secret.json",
            scopes=["openid", "https://www.googleapis.com/auth/userinfo.email"],
            state=state,
        )
        flow.redirect_uri = f"{BACK_URL}/api/v1/user/google/callback"

        code = request.query_params["code"]
        flow.fetch_token(code=code)
        credentials = flow.credentials
        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {credentials.token}"})
        userinfo_response = session.get("https://www.googleapis.com/oauth2/v1/userinfo")

        if userinfo_response.ok:
            userinfo = userinfo_response.json()
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
