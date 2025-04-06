import hashlib

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import FileVersion


@receiver(pre_save, sender=FileVersion)
def set_file_hash(sender, instance, **kwargs):
    if not instance.file_hash and instance.file_content:
        hasher = hashlib.sha256()
        for chunk in instance.file_content.chunks():
            hasher.update(chunk)
        instance.file_hash = hasher.hexdigest()


@receiver(pre_save, sender=FileVersion)
def set_version_number(sender, instance, **kwargs):
    if not instance.version_number:
        last_version = FileVersion.objects.filter(file=instance.file).order_by('-version_number').first()
        if last_version:
            instance.version_number = last_version.version_number + 1
        else:
            instance.version_number = 1
