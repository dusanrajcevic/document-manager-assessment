from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from propylon_document_manager.file_versions.models import FileVersion

class FileVersionsTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email="test@test.com", password="pass")
        self.user2 = User.objects.create_user(email="test2@test.com", password="pass")

        self.client.force_authenticate(user=self.user)

        self.file_v1 = FileVersion.objects.create(
            file_name="example.txt",
            version_number=1,
            file_content=SimpleUploadedFile("example.txt", b"test file content"),
            file_path="/documents/example.txt",
            uploaded_by=self.user,
        )

        self.file_v2 = FileVersion.objects.create(
            file_name="example.txt",
            version_number=2,
            file_content=SimpleUploadedFile("example_v2.txt", b"version 2 content"),
            file_path="/documents/example.txt",
            uploaded_by=self.user,
        )

    def test_file_version_upload(self):
        self.client.force_authenticate(user=self.user)
        file_data = {
            "file_name": "example.txt",
            "file_path": "/documents/example.txt",
            "file_content": SimpleUploadedFile("example.txt", b"test file content"),
        }
        response = self.client.post(
            path="/api/file_versions/",
            data=file_data,
            format="multipart"
        )
        files = FileVersion.objects.all()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2 from setUp and 1 from the test
        self.assertEqual(files.count(), 3)
        self.assertEqual(files[2].file_name, "example.txt")
        self.assertEqual(files[2].version_number, 3)
