import io
import random
from collections.abc import Sequence
from typing import Any

from django.contrib.auth import get_user_model
from factory import Faker, post_generation, LazyAttribute, SubFactory, Sequence as FactorySequence
from factory.django import DjangoModelFactory, FileField

from propylon_document_manager.file_versions.models import File, FileVersion


class UserFactory(DjangoModelFactory):
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["email"]
        skip_postgeneration_save = True


class FileFactory(DjangoModelFactory):
    class Meta:
        model = File

    file_name = Faker("file_name")
    file_path = LazyAttribute(lambda o: f"/documents/{o.file_name}")
    uploaded_by = SubFactory(UserFactory)
    uploaded_at = Faker("date_time")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if "uploaded_by" in kwargs:
            kwargs["uploaded_by"] = kwargs.pop("uploaded_by")
        else:
            kwargs["uploaded_by"] = UserFactory()
        return super()._create(model_class, *args, **kwargs)


class FileVersionFactory(DjangoModelFactory):
    class Meta:
        model = FileVersion

    file = SubFactory(FileFactory)
    version_number = FactorySequence(lambda n: n + 1)

    file_content = FileField(
        from_func=lambda: io.BytesIO(f"File content {random.randint(1, 100000)}".encode())
    )

    uploaded_at = Faker("date_time")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        uploaded_by = kwargs.pop("uploaded_by", None)
        file = kwargs.pop("file", None)

        # If no file is provided, create one with or without uploaded_by
        if file is None:
            if uploaded_by is not None:
                file = FileFactory(uploaded_by=uploaded_by)
            else:
                file = FileFactory()

        # Ensure file is added to kwargs
        kwargs["file"] = file

        return super()._create(model_class, *args, **kwargs)
