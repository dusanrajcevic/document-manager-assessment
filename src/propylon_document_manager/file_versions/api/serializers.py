from rest_framework import serializers

from ..models import FileVersion

class FileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileVersion
        fields = "__all__"
        extra_kwargs = {
            "uploaded_by": {"required": False},
        }
