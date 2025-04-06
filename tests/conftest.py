import pytest

from rest_framework.test import APIClient
from propylon_document_manager.file_versions.models import User, File, FileVersion
from .factories import UserFactory, FileFactory, FileVersionFactory


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def users(db) -> list[User]:
    return UserFactory.create_batch(3)


@pytest.fixture
def file(db, user) -> File:
    return FileFactory()


@pytest.fixture
def files(db, user) -> list[File]:
    return FileFactory.create_batch(3, uploaded_by=user)


@pytest.fixture
def file_versions(db, file) -> list[FileVersion]:
    return FileVersionFactory.create_batch(3, file=file)


@pytest.fixture
def api_client():
    return APIClient()
