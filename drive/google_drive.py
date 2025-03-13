import requests
import os
from django.conf import settings

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_DRIVE_METADATA_URL = "https://www.googleapis.com/drive/v3/files/{}?fields=name,mimeType"


def upload_file_to_drive(access_token: str, file_path: str, file_name: str) -> dict:
    """Upload a file to Google Drive."""
    headers = {"Authorization": f"Bearer {access_token}"}
    metadata = {"name": file_name}
    files = {
        "data": ("metadata", str(metadata), "application/json"),
        "file": open(settings.MEDIA_ROOT + "/" + file_path, "rb"),
    }

    response = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files,
    )

    # Delete the file from the server after uploading
    os.remove(settings.MEDIA_ROOT + "/" + file_path)

    return response.json()


def list_drive_files(access_token: str) -> dict:
    """List user's Google Drive files."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://www.googleapis.com/drive/v3/files", headers=headers)
    return response.json()


def download_drive_file(access_token: str, file_id: str) -> dict | None:
    """Download a file from Google Drive."""
    headers = {"Authorization": f"Bearer {access_token}"}

    metadata_response = requests.get(GOOGLE_DRIVE_METADATA_URL.format(file_id), headers=headers)
    if metadata_response.status_code != 200:
        return None

    metadata = metadata_response.json()
    file_name = metadata.get("name", f"{file_id}")

    download_url = f"https://www.googleapis.com/drive/v3/files/{file_id}/?alt=media"
    response = requests.get(download_url, headers=headers)

    if response.status_code == 200:
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        return {"message": "File downloaded successfully", "path": file_path}
    else:
        return None
