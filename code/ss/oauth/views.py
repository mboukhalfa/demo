from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from oauth.forms import OauthAppForm, DeleteOauthAppForm
from oauth.models import OauthApp
import requests
import base64
from django.conf import settings

'''
 SETTINGS
	  '''
UUID_EXPIRE_SECONDS = settings.UUID_EXPIRE_SECONDS
WEB_SERVER_URL_ROOT = settings.WEB_SERVER_URL_ROOT
WEB_SERVER_URL_API_UPLOAD = settings.WEB_SERVER_URL_API_UPLOAD

url = settings.SERVER_URL_ROOT


@login_required
@staff_member_required
def gettokens(request):
    if request.method == 'POST':

        # Create new Oauth app instance
        form = OauthAppForm(request.POST)

        if form.is_valid():
            # we should have only one Oauth app in db
            if OauthApp.objects.all().count():
                OauthApp.objects.all().delete()

            oauthAppObject = form.save()

            context = {
                'url': url,
                'oauthAppObject': oauthAppObject,
            }
            return render(request, "oauth/OauthApp.html", context)

        else:
            context = {
                "form": form,
            }
            return render(request, "oauth/addOauthApp.html", context)

    # if a GET
    elif request.method == 'GET':
        # if Oauth app exist
        if OauthApp.objects.all().count():

            oauthAppObject = OauthApp.objects.all().first()
            # if there is a code param then its redirect from owner authorization
            if not request.GET.get('code'):

                # show app info and buttons for get tokens , edit app and delete
                # form = OauthAppForm(instance=oauthAppObject)
                context = {
                    'url': url,
                    'oauthAppObject': oauthAppObject,
                }
                return render(request, "oauth/OauthApp.html", context)

            else:
                post_data = {'code': request.GET["code"], 'redirect_uri': oauthAppObject.redirect_uri,
                             'grant_type': "authorization_code"}
                client_id = oauthAppObject.client_id.encode()
                client_secret = oauthAppObject.client_secret.encode()
                bb64 = base64.b64encode(client_id + b":" + client_secret)
                bs = bb64.decode("utf-8")
                response = requests.post(WEB_SERVER_URL_ROOT + '/o/token/', data=post_data,
                                         headers={'Authorization': 'Basic ' + bs})

                if response:
                    json_data = response.json()
                    # response content is json TODO parse it and store the acces and refresh tokens
                    oauthAppObject.access_token = json_data["access_token"]
                    oauthAppObject.refresh_token = json_data["refresh_token"]
                    oauthAppObject.save()

                else:
                    return HttpResponse("no response from server web ", status=444)

                context = {
                    'oauthAppObject': oauthAppObject,
                    'url': url,
                }
                return render(request, "oauth/OauthApp.html", context)

        else:
            # show new form to add new Oauth
            form = OauthAppForm()

            context = {
                "form": form,
            }

            return render(request, "oauth/addOauthApp.html", context)


@login_required(login_url='/admin/')
@staff_member_required
def deleteOauthApp(request):
    if request.method == 'POST':

        if OauthApp.objects.all().count():
            OauthApp.objects.all().delete()

        form = OauthAppForm()
        context = {
            "form": form,
        }
        return render(request, "oauth/addOauthApp.html", context)
    else:
        if not OauthApp.objects.all().count():
            return redirect('oauth:gettokens')
        # show new form to add new Oauth
        form = DeleteOauthAppForm()

        context = {
            "form": form,
        }

        return render(request, "oauth/deleteOauthApp.html", context)
