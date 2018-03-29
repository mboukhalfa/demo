from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^upload/gettokens/$', views.gettokens, name='gettokens'),
    url(r'^upload/deleteOauthApp/$', views.deleteOauthApp, name='deleteOauthApp'),
]
