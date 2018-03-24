from rest_framework import generics

from upload.models import Video
from .serializers import UploadUUIDSerializer

class UploadUUIDRetrieveAPIView(generics.RetrieveAPIView):
	lookup_field = "uuid"#23e22a3d-a836-4f0b-8e36-e86c059dec8d
	serializer_class = UploadUUIDSerializer
	queryset = Video.objects.all()