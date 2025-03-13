import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


@api_view(["GET"])
def google_login(request: Request) -> Response:
    """Redirects user to Google OAuth2.0 login page"""
    auth_url = (
        f"{GOOGLE_AUTH_URL}?response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        f"&scope=openid email profile"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return Response({"auth_url": auth_url}, status=status.HTTP_200_OK)


@api_view(["GET"])
def google_callback(request: Request) -> Response:
    """Callback function for Google OAuth2.0"""
    code = request.GET.get("code")
    if not code:
        return Response({"error": "Authorization code not provided"}, status=status.HTTP_400_BAD_REQUEST)

    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    token_data = response.json()

    if "access_token" not in token_data:
        return Response({"error": "Failed to retrieve access token"}, status=status.HTTP_400_BAD_REQUEST)

    access_token = token_data["access_token"]

    # Fetch user info
    user_info = requests.get(GOOGLE_USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"}).json()

    return Response({"user_info": user_info, "access_token": access_token}, status=status.HTTP_200_OK)
