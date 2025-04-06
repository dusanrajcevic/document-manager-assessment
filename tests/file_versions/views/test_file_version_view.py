from rest_framework import status

from tests.factories import FileVersionFactory, FileFactory


def test_file_version_retrieve(api_client, user, files):
    file_v3 = files[2]
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/documents{file_v3.file_path}")
    assert response.status_code == status.HTTP_200_OK


def test_file_version_retrieve_access_denied(api_client, user, users, files):
    file = files[0]
    api_client.force_authenticate(user=users[0])
    response = api_client.get(f"/documents{file.file_path}")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_file_version_filter_by_id(api_client, user, file, file_versions):
    api_client.force_authenticate(user=user)
    file2 = FileFactory(uploaded_by=user)
    FileVersionFactory.create_batch(2, file=file2)
    response = api_client.get(f"/api/file_versions/?file={file_versions[0].id}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3  # 3 versions from file_versions fixture


def test_file_version_list(api_client, user, file, file_versions):
    api_client.force_authenticate(user=user)
    file2 = FileFactory(uploaded_by=user)
    FileVersionFactory.create_batch(2, file=file2)
    response = api_client.get(f"/api/file_versions/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5  # 3 versions from file_versions fixture + 2 from file2


def test_file_version_retrieve_by_hash(api_client, user):
    api_client.force_authenticate(user=user)
    file = FileFactory(uploaded_by=user)
    versions = FileVersionFactory.create_batch(1, file=file)

    file_hash = versions[0].file_hash

    url = "/api/file_versions/by-hash/" + file_hash + '/'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == versions[0].id
    assert response.data["file_hash"]
