from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from src.votaciones.settings import BACK_URL, UCO_CLIENT_ID, UCO_SECRET_ID, UCO_AUTHORIZATION_URL, UCO_TOKEN_URL
from authlib.integrations.django_client import OAuth

class UCOLoginRedirectController(APIView):
    http_method_names = ["get"]

    def get(self, request: Request) -> Response:
        oauth = OAuth()

        oauth.register(
            name='uco',
            client_id=UCO_CLIENT_ID,
            client_secret=UCO_SECRET_ID,
            authorize_url=UCO_AUTHORIZATION_URL,
            token_url=UCO_TOKEN_URL,
            client_kwargs={'scope': 'email'},
        )
        redirect_uri=f"{BACK_URL}/login/uco/callback"
        return oauth.provider.authorize_redirect(request, redirect_uri)