import pytest
from propylon_document_manager.file_versions.models import User


def test_create_superuser():
    email = "admin@example.com"
    password = "supersecurepassword"

    superuser = User.objects.create_superuser(email=email, password=password)

    assert superuser.email == email
    assert superuser.is_staff
    assert superuser.is_superuser
    assert superuser.check_password(password)


def test_superuser_requires_email():
    with pytest.raises(ValueError, match="The Email field must be set"):
        User.objects.create_superuser(email=None, password="supersecurepassword")
