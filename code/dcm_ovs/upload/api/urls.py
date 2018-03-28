from django.conf.urls import url
from .views import UploadUUIDRetrieveAPIView

urlpatterns = [
	url(r'^secret/$', 'upload.api.views.secret_page', name='secret'),
    url(r'^(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', UploadUUIDRetrieveAPIView.as_view(), name='Upload-UUID-retrieve'),
]
