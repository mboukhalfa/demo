from rest_framework import generics

from oauth2_provider.views.generic import ProtectedResourceView

from upload.models import Video
from .serializers import UploadUUIDSerializer

# ProtectedResourceView,

from rest_framework import permissions

from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UploadUUIDRetrieveAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = (permissions.IsAdminUser,)
    lookup_field = "uuid"
    serializer_class = UploadUUIDSerializer
    queryset = Video.objects.all()
