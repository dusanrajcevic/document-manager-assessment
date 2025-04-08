import hashlib

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import FileVersion


@receiver(pre_save, sender=FileVersion)
def set_file_hash(sender, instance, **kwargs):
    if instance.file_hash or not instance.file_content:
        return

    hasher = hashlib.sha256()
    for chunk in instance.file_content.chunks():
        hasher.update(chunk)

    user_id = str(instance.file.uploaded_by_id) if instance.file and instance.file.uploaded_by_id else 'anonymous'
    hasher.update(user_id.encode())

    instance.file_hash = hasher.hexdigest()


@receiver(pre_save, sender=FileVersion)
def set_version_number(sender, instance, **kwargs):
    if instance.version_number:
        return

    last_version = (FileVersion.objects
                    .filter(file=instance.file)
                    .order_by('-version_number')
                    .first())
    instance.version_number = last_version.version_number + 1 if last_version else 1
