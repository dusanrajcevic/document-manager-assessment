import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from propylon_document_manager.file_versions.models import FileVersion, File
from django.core.files.uploadedfile import SimpleUploadedFile

from propylon_document_manager.site.settings.base import BASE_DIR

files = [
    {
        "file_name": "document_1",
        "file_path": "/documents/document_1.txt",
    },
    {
        "file_name": "document_2",
        "file_path": "/documents/document_2.txt",
    },
]

file_versions = [
    {
        "version_number": 1,
        "file_content": SimpleUploadedFile("document_1_v1.txt", b"Document 1 version 1 content"),
        "file_name": "document_1",  # Reference to the file name in `files`
    },
    {
        "version_number": 2,
        "file_content": SimpleUploadedFile("document_1_v2.txt", b"Document 1 version 2 content"),
        "file_name": "document_1",
    },
    {
        "version_number": 1,
        "file_content": SimpleUploadedFile("document_2_v1.txt", b"Document 2 version 1 content"),
        "file_name": "document_2",
    },
]


class Command(BaseCommand):
    help = "Load basic file and file version fixtures"

    def create_static_dir_if_not_exists(self):
        static_dir = os.path.join(BASE_DIR, "static")
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
            self.stdout.write(self.style.SUCCESS(f"Created directory: {static_dir}"))

    def handle(self, *args, **options):
        self.create_static_dir_if_not_exists()

        user = get_user_model().objects.first()
        if not user:
            self.stderr.write(self.style.ERROR("No user exists. Please create a user first."))
            return

        file_mapping = {}
        for file_data in files:
            file_instance = File.objects.create(
                file_name=file_data["file_name"],
                file_path=file_data["file_path"],
                uploaded_by=user,
            )
            file_mapping[file_data["file_name"]] = file_instance

        for file_version_data in file_versions:
            FileVersion.objects.create(
                file=file_mapping[file_version_data["file_name"]],
                version_number=file_version_data["version_number"],
                file_content=file_version_data["file_content"],
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {len(files)} files and {len(file_versions)} file versions.")
        )
