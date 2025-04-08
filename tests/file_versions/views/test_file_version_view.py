import pytest
from rest_framework import status

from tests.factories import FileVersionFactory, FileFactory, UserFactory


@pytest.mark.django_db
def test_file_version_filter_by_id(api_client, user, file_with_versions):
    FileVersionFactory.create_batch(2, file=FileFactory(uploaded_by=user))

    api_client.force_authenticate(user=user)
    response = api_client.get(f"/api/file_versions/?file={file_with_versions.id}")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3  # 3 fixtures


@pytest.mark.django_db
def test_file_version_all(api_client, user):
    number_of_files = 5
    FileVersionFactory.create_batch(number_of_files, file=FileFactory(uploaded_by=user))
    FileVersionFactory.create_batch(number_of_files, file=FileFactory(uploaded_by=user))
    FileVersionFactory.create_batch(number_of_files, file=FileFactory(uploaded_by=user))

    api_client.force_authenticate(user=user)
    response = api_client.get(f"/api/file_versions/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3 * number_of_files


@pytest.mark.django_db
def test_file_version_all_only_current_user(api_client, user):
    user2 = UserFactory()

    FileVersionFactory.create_batch(2, file=FileFactory(uploaded_by=user))
    FileVersionFactory.create_batch(3, file=FileFactory(uploaded_by=user))
    FileVersionFactory.create_batch(10, file=FileFactory(uploaded_by=user2))

    api_client.force_authenticate(user=user)
    response = api_client.get(f"/api/file_versions/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2 + 3


@pytest.mark.django_db
def test_file_version_retrieve_by_hash(api_client, user):
    api_client.force_authenticate(user=user)
    versions = FileVersionFactory.create_batch(1, file=FileFactory(uploaded_by=user))

    file_hash = versions[0].file_hash

    url = "/api/file_versions/by-hash/" + file_hash + '/'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["version_number"] == versions[0].version_number
    assert response.data["file_hash"] == file_hash
    assert response.data["file"]["id"] == versions[0].id


@pytest.mark.django_db
def test_file_version_retrieve_by_hash_access_denied(api_client, user):
    user2 = UserFactory()
    api_client.force_authenticate(user=user)
    versions = FileVersionFactory.create_batch(1, file=FileFactory(uploaded_by=user2))

    file_hash = versions[0].file_hash

    url = "/api/file_versions/by-hash/" + file_hash + '/'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_file_version_retrieve_by_wrong_hash(api_client, user):
    user2 = UserFactory()
    api_client.force_authenticate(user=user)
    versions = FileVersionFactory.create_batch(1, file=FileFactory(uploaded_by=user2))

    file_hash = versions[0].file_hash

    url = "/api/file_versions/by-hash/wrong" + file_hash + 'hash/'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
