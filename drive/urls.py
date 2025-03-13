from django.urls import path
from .views import connect_google_drive, upload_file, list_files, download_file

urlpatterns = [
    path("connect/", connect_google_drive, name="connect_google_drive"),
    path("upload/", upload_file, name="upload_file"),
    path("files/", list_files, name="list_files"),
    path("download/<str:file_id>/", download_file, name="download_file"),
]
