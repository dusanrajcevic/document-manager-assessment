from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from propylon_document_manager.file_versions.models import FileVersion
from django.core.files.uploadedfile import SimpleUploadedFile

file_versions = [
    {
        "file_name": "document_1",
        "file_path": "/documents/document_1.txt",
        "file_content": SimpleUploadedFile("document_1.txt", b"Document 1 content"),
    },
    {
        "file_name": "document_2",
        "file_path": "/documents/document_2.txt",
        "file_content": SimpleUploadedFile("document_2.txt", b"Document 2 content"),
    },
    {
        "file_name": "document_3",
        "file_path": "/documents/document_3.txt",
        "file_content": SimpleUploadedFile("document_3.txt", b"Document 3 content"),
    },
    {
        "file_name": "document_4",
        "file_path": "/documents/document_4.txt",
        "file_content": SimpleUploadedFile("document_4.txt", b"Document 4 content"),
    },
]

class Command(BaseCommand):
    help = "Load basic file version fixtures"

    def handle(self, *args, **options):
        user = get_user_model().objects.first()
        if not user:
            self.stderr.write(self.style.ERROR("No user exists. Please create a user first."))
            return

        for file_data in file_versions:
            FileVersion.objects.create(
                file_name=file_data["file_name"],
                file_path=file_data["file_path"],
                file_content=file_data["file_content"],
                uploaded_by=user,
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {len(file_versions)} file versions.")
        )
