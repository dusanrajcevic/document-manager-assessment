from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from urllib.parse import unquote

from ..models import FileVersion, File
from .serializers import FileVersionSerializer, FileUploadSerializer


class IsUploader(BasePermission):
    """
    Custom permission class to ensure that only the uploader can access or modify the file version.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, File):
            return obj.uploaded_by == request.user
        if isinstance(obj, FileVersion):
            return obj.file.uploaded_by == request.user
        return False


class FileUploadViewSet(CreateModelMixin, GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FileUploadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_version = serializer.save()

        response_data = {
            "file_name": file_version.file.file_name,
            "file_path": file_version.file.file_path,
            "version_number": file_version.version_number,
            "file_hash": file_version.file_hash,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):
    """
    ViewSet for managing FileVersion objects.
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsUploader]
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        """
        Optionally filters the queryset by 'file' or 'file_path' query parameters.
        """
        file_id = self.request.query_params.get("file")

        if file_id:
            return FileVersion.objects.select_related('file').filter(file_id=file_id)
        return FileVersion.objects.select_related('file').all()

    @action(detail=False, methods=["get"], url_path="by-hash/(?P<file_hash>[^/.]+)")
    def retrieve_by_hash(self, request, file_hash=None):
        """
        Retrieve a file version by its hash (optional).
        """
        try:
            file_version = FileVersion.objects.get(file_hash=file_hash)
            self.check_object_permissions(request, file_version)  # Apply custom permissions
            serializer = self.get_serializer(file_version)
            return Response(serializer.data)
        except FileVersion.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def serve_file_version(request, file_path=None):
    """
    Serve the latest or a specific version of a file based on the file_path and revision query param.
    """
    file_path = unquote(file_path)
    revision = request.query_params.get("revision")

    try:
        file = File.objects.get(file_path=f"/{file_path}")
    except File.DoesNotExist:
        return Response({"detail": "File not found or revision does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if file.uploaded_by != request.user:
        return Response({"detail": "You do not have permission to access this file."}, status=403)

    try:
        if revision is not None:
            file_version = file.versions.get(version_number=int(revision))
        else:
            file_version = file.versions.order_by("-version_number").first()
    except FileVersion.DoesNotExist:
        return Response({"detail": "File not found or revision does not exist."}, status=status.HTTP_404_NOT_FOUND)

    serializer = FileVersionSerializer(file_version)
    return Response(serializer.data)
