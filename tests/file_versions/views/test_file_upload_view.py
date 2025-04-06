import hashlib

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status


def test_file_upload(api_client, user):
    file_name = "example_v3.txt"
    file_path = "/documents/example_v3.txt"
    file_content = b"test file content for version 3"
    file = SimpleUploadedFile(file_name, b"test file content for version 3")
    api_client.force_authenticate(user=user)

    file_data = {
        "file_name": file_name,
        "file_path": file_path,
        "file": file,
    }
    response = api_client.post(
        path="/api/upload/",
        data=file_data,
        format="multipart"
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED

    assert response_data['file_name'] == file_name
    assert response_data['file_path'] == file_path
    assert response_data['version_number'] == 1
    assert response_data['file_hash'] == hashlib.sha256(file_content).hexdigest()
