import hashlib

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status


def test_file_upload(api_client, user):
    file_name = "example.txt"
    file_path = "/documents/example.txt"
    file_content = b"test file content for version 1"
    file_upload_and_assert(
        api_client=api_client,
        user=user,
        file_name=file_name,
        file_path=file_path,
        file_content=file_content,
        version_number=1
    )


def test_file_upload_higher_version(api_client, user, file_with_versions):
    file_name = file_with_versions.file_name
    file_path = file_with_versions.file_path
    file_content = b"test file content for version 3"
    file_upload_and_assert(
        api_client=api_client,
        user=user,
        file_name=file_name,
        file_path=file_path,
        file_content=file_content,
        version_number=4
    )

def test_duplicate_file_upload_same_user(api_client, user):
    file_name = "duplicate.txt"
    file_path = "/documents/duplicate.txt"
    file_content = b"identical file content"

    file_upload_and_assert(
        api_client=api_client,
        user=user,
        file_name=file_name,
        file_path=file_path,
        file_content=file_content,
        version_number=1,
    )

    file = SimpleUploadedFile(name=file_name, content=file_content)
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

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.data["detail"] == 'This file already exists. Duplicate uploads are not allowed.'



def file_upload_and_assert(api_client, user, file_name, file_path, file_content, version_number):
    """
    Helper function to assert file upload response.
    """
    file = SimpleUploadedFile(name=file_name, content=file_content)
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

    hasher = hashlib.sha256()
    hasher.update(file_content)
    hasher.update(str(user.id).encode())

    assert response_data['file_name'] == file_name
    assert response_data['file_path'] == file_path
    assert response_data['version_number'] == version_number
    assert response_data['file_hash'] == hasher.hexdigest()
