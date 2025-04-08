from rest_framework import serializers

from ..models import FileVersion, File


class FileUploadSerializer(serializers.Serializer):
    file_name = serializers.CharField(max_length=512)
    file_path = serializers.CharField(max_length=512)
    file = serializers.FileField()

    def create(self, validated_data):
        user = self.context['request'].user

        file_name = validated_data['file_name']
        file_content = validated_data['file']
        file_path = validated_data['file_path']
        if not file_path.startswith('/'):
            file_path = '/' + file_path

        file, created = File.objects.get_or_create(
            file_path=file_path,
            uploaded_by=user,
            defaults={'file_name': file_name}
        )

        file_version = FileVersion.objects.create(
            file=file,
            file_content=file_content
        )

        return file_version


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


class FileVersionSerializer(serializers.ModelSerializer):
    file = FileSerializer()

    class Meta:
        model = FileVersion
        fields = "version_number", "file_hash", "uploaded_at", "file"
        extra_kwargs = {
            "uploaded_by": {"required": False},
            "file": {"required": True},
        }
