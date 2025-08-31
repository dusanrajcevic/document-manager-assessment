from propylon_document_manager.file_versions.models import User


def test_save_user_password(user):
    user = User.objects.create_user(email="test@test.com", password="password123")

    assert user.check_password("password123")


def test_update_user_password(user):
    password = 'password123'
    user.password = password
    user.save()

    assert user.check_password(password)
