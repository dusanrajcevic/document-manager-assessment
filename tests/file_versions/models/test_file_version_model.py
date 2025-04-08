import hashlib
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile

from propylon_document_manager.file_versions.models import File, FileVersion, User


def test_file_version_model(user, file):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"Test content for version 1")
        temp_file.seek(0)
        file_content = SimpleUploadedFile(temp_file.name, temp_file.read())

    FileVersion.objects.create(
        file=file,
        version_number=1,
        file_content=file_content,
    )

    file_versions = FileVersion.objects.all()
    file_content.seek(0)

    assert file_versions.count() == 1
    assert file_versions[0].file == file
    assert file_versions[0].version_number == 1
    assert file_versions[0].file_content.name == f"documents/{file_content.name}"
    assert file_versions[0].file_hash is not None
    assert file_versions[0].file_content.read() == file_content.read()

    assert str(file_versions[0]) == f"{file.file_name} (Revision 1, Hash: {file_versions[0].file_hash[:8]})"

    file_content.close()


def test_set_file_hash_signal(user, file):
    file_content = SimpleUploadedFile("example.txt", b"Test file content")
    file_version = FileVersion.objects.create(file=file, file_content=file_content)

    hasher = hashlib.sha256()
    hasher.update(b"Test file content")
    hasher.update(str(file_version.file.uploaded_by.id).encode())

    expected_hash = hasher.hexdigest()
    assert file_version.file_hash == expected_hash


def test_set_version_number_signal(user, file):
    file_content_1 = SimpleUploadedFile("example1.txt", b"Test file content 1")
    file_content_2 = SimpleUploadedFile("example2.txt", b"Test file content 2")

    file_version_1 = FileVersion.objects.create(file=file, file_content=file_content_1)
    assert file_version_1.version_number == 1

    file_version_2 = FileVersion.objects.create(file=file, file_content=file_content_2)
    assert file_version_2.version_number == 2
