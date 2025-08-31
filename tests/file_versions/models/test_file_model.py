from propylon_document_manager.file_versions.models import File


def test_file_model(user):
    file_name = "test_file.txt"
    file_path = "/documents/test_file.txt"

    File.objects.create(
        file_name=file_name,
        file_path=file_path,
        uploaded_by=user,
    )

    files = File.objects.all()

    assert files.count() == 1
    assert files[0].file_name == file_name
    assert files[0].file_path == file_path
    assert files[0].uploaded_by == user

    assert str(files[0]) == f"{file_path} owned by {user.email}"
