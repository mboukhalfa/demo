from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^gettokens/$', views.gettokens, name='gettokens'),
    url(r'^deleteOauthApp/$', views.deleteOauthApp, name='deleteOauthApp'),
]
