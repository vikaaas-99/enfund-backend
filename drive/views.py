from django.conf import settings
from .google_drive import upload_file_to_drive, list_drive_files, download_drive_file
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.request import Request

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"


@api_view(["GET"])
def connect_google_drive(request: Request) -> Response:
    """Generate Google OAuth URL for connecting to Google Drive."""
    auth_url = (
        f"{GOOGLE_AUTH_URL}?response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        f"&scope=https://www.googleapis.com/auth/drive.file"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return Response({"auth_url": auth_url}, status=HTTP_200_OK)


@api_view(["POST"])
def upload_file(request: Request) -> Response:
    """Upload a file to Google Drive."""
    access_token = request.data.get("access_token")
    file = request.FILES.get("file")

    if not access_token or not file:
        return Response({"error": "Access token and file required"}, status=HTTP_400_BAD_REQUEST)

    file_path = default_storage.save(file.name, ContentFile(file.read()))
    response = upload_file_to_drive(access_token, file_path, file.name)

    return Response(response, status=HTTP_200_OK)


@api_view(["GET"])
def list_files(request: Request) -> Response:
    """Fetch files from Google Drive."""
    access_token = request.GET.get("access_token")
    if not access_token:
        return Response({"error": "Access token required"}, status=HTTP_400_BAD_REQUEST)

    response = list_drive_files(access_token)
    return Response(response, status=HTTP_200_OK)


@api_view(["GET"])
def download_file(request: Request, file_id: str) -> Response:
    """Download a file from Google Drive."""
    access_token = request.GET.get("access_token")
    if not access_token:
        return Response({"error": "Access token required"}, status=HTTP_400_BAD_REQUEST)

    response = download_drive_file(access_token, file_id)
    if response:
        return Response(response, status=HTTP_200_OK)
    else:
        return Response({"error": "File not found"}, status=HTTP_400_BAD_REQUEST)
