from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ..models import FileVersion
from .serializers import FileVersionSerializer

class IsUploader(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.uploaded_by == request.user

class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsUploader]
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()
    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(uploaded_by=request.user)  # Associate the logged-in user
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        file_path = self.request.query_params.get("file_path")

        return FileVersion.objects.filter(file_path=file_path) if file_path else FileVersion.objects.all()
