from rest_framework import status


def test_file_retrieve(api_client, user, file_with_versions):
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/documents{file_with_versions.file_path}")

    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Disposition"] == f'attachment; filename="{file_with_versions.file_name}.txt"'


def test_file_retrieve_with_revision(api_client, user, file_with_versions):
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/documents{file_with_versions.file_path}?revision=1")

    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Disposition"] == f'attachment; filename="{file_with_versions.file_name}.txt"'


def test_file_retrieve_with_wrong_revision(api_client, user, file_with_versions):
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/documents{file_with_versions.file_path}?revision=5")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "File not found or revision does not exist."


def test_file_retrieve_access_denied(api_client, user, file_with_versions, users):
    api_client.force_authenticate(user=users[0])
    response = api_client.get(f"/documents{file_with_versions.file_path}")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["detail"] == "You do not have permission to access this file."

