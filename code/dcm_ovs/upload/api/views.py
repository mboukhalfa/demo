from rest_framework import generics

from oauth2_provider.views.generic import ProtectedResourceView

from upload.models import Video
from .serializers import UploadUUIDSerializer


# ProtectedResourceView,

from rest_framework import permissions
# from upload.api.permissions import IsAdmin


class UploadUUIDRetrieveAPIView(generics.RetrieveAPIView):
	permission_classes = (permissions.IsAuthenticated,
                      permissions.IsAdminUser,)
	lookup_field = "uuid"#23e22a3d-a836-4f0b-8e36-e86c059dec8d
	serializer_class = UploadUUIDSerializer
	queryset = Video.objects.all()

