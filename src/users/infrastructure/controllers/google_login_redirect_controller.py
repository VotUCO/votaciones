from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import redirect
from src.votaciones.settings import BACK_URL

import google_auth_oauthlib.flow


class GoogleLoginRedirectController(APIView):
    http_method_names = ["get"]

    def get(self, request: Request) -> Response:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            "client_secret.json",
            scopes=["openid", "https://www.googleapis.com/auth/userinfo.email"],
        )

        flow.redirect_uri = f"{BACK_URL}/api/v1/user/google/callback"

        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Recommended, enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type="offline",
            # Optional, enable incremental authorization. Recommended as a best practice.
            include_granted_scopes="true",
        )
        request.session["state"] = state
        return redirect(authorization_url)
