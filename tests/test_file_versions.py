from propylon_document_manager.file_versions.models import FileVersion
from django.contrib.auth import get_user_model

def test_file_versions():
    file_name = "new_file"
    file_version = 1
    file_content = "documents/test.txt"
    file_path = "documents/reviews/test.txt"
    test_user = get_user_model().objects.create_user(email="test@test.com", password="pass")

    # Create a FileVersion instance
    FileVersion.objects.create(
        file_name=file_name,
        version_number=file_version,
        file_content=file_content,
        file_path=file_path,
        uploaded_by=test_user,
    )
    files = FileVersion.objects.all()
    assert files.count() == 1
    assert files[0].file_name == file_name
    assert files[0].version_number == file_version
    assert files[0].file_content == file_content
    assert files[0].file_path == file_path
    assert files[0].uploaded_by == test_user

