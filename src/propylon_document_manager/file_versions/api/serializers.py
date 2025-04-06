from rest_framework import serializers

from ..models import FileVersion, File


class FileUploadSerializer(serializers.Serializer):
    file_name = serializers.CharField(max_length=512)
    file_path = serializers.CharField(max_length=512)
    file = serializers.FileField()

    def create(self, validated_data):
        user = self.context['request'].user

        file = File.objects.create(
            file_name=validated_data['file_name'],
            file_path=validated_data['file_path'],
            uploaded_by=user
        )

        file_version = FileVersion.objects.create(
            file=file,
            file_content=validated_data['file'],
        )

        return file_version


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


class FileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileVersion
        fields = "__all__"
        extra_kwargs = {
            "uploaded_by": {"required": False},
            "file": {"required": True},
        }
