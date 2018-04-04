from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.views.decorators.csrf import csrf_exempt
from upload.forms import OauthAppForm, DeleteOauthAppForm
from shutil import move
from django.utils.timezone import utc
from django.utils.dateparse import parse_datetime

import datetime
import requests
import base64

from upload.models import OauthApp

from .validator.validator import VideoValidator

'''
 SETTINGS
	  '''
UUID_EXPIRE_SECONDS = 300
WEB_SERVER_URL_ROOT = 'http://web_dcm_ovs:8000'
WEB_SERVER_URL_API_UPLOAD = '/api/upload/'


@csrf_exempt
def upload(request):
    if request.method == 'POST':

        for i in range(1, 3):

            if OauthApp.objects.all().count():
                oauthAppObject = OauthApp.objects.all().first()
                if not oauthAppObject.access_token:
                    return HttpResponse("no access token ", status=403)
            else:
                raise PermissionDenied

            uuid = request.POST['uuid']
            # check if uuid is valid
            response = requests.get(WEB_SERVER_URL_ROOT + WEB_SERVER_URL_API_UPLOAD + uuid + '/',
                                    headers={'Authorization': 'Bearer ' + oauthAppObject.access_token})

            if response:
                # if valide time and not uploaded
                json_data = response.json()
                timediff = datetime.datetime.utcnow().replace(tzinfo=utc) - parse_datetime(json_data['timestamp'])
                if not json_data['uploaded'] and timediff.total_seconds() < UUID_EXPIRE_SECONDS:
                    # validate video
                    v_v = VideoValidator(request.POST)
                    if not v_v.is_valid():
                        return HttpResponse("Unsupported Media Type", status=415)

                    # inform website that video uploaded
                    r = requests.put(WEB_SERVER_URL_ROOT + WEB_SERVER_URL_API_UPLOAD + uuid + '/',
                                     headers={'Authorization': 'Bearer ' + oauthAppObject.access_token},
                                     data={'uploaded': True})

                    if r:
                        # from mime type in VideoValidator we can find ext than rename file
                        move(request.POST["file.path"], "/upload/" + request.POST["file.name"])
                        return HttpResponse("uploaded ")

                    else:
                        return HttpResponse("unable confirm upload", status=504)


                else:

                    raise PermissionDenied  # maybe we can inform that this uuid not valid
            #  else maybe because of access token or UUID non valide
            else:
                # if uuid not valide
                if response.status_code == requests.codes['not_found']:
                    raise Http404

                post_data = {'grant_type': 'refresh_token', 'client_id': oauthAppObject.client_id,
                             'client_secret': oauthAppObject.client_secret,
                             'refresh_token': oauthAppObject.refresh_token}
                response = requests.post(WEB_SERVER_URL_ROOT + '/o/token/', data=post_data)

                if response:
                    json_data = response.json()
                    oauthAppObject.access_token = json_data["access_token"]
                    oauthAppObject.refresh_token = json_data["refresh_token"]
                    oauthAppObject.save()

    return HttpResponse("no response from server web ", status=444)


@login_required(login_url='/admin/')
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
                'oauthAppObject': oauthAppObject,
            }
            return render(request, "upload/OauthApp.html", context)

        else:
            context = {
                "form": form,
            }
            return render(request, "upload/addOauthApp.html", context)

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
                    # "form":form,
                    'oauthAppObject': oauthAppObject,
                }
                return render(request, "upload/OauthApp.html", context)

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
                }
                return render(request, "upload/OauthApp.html", context)

        else:
            # show new form to add new Oauth
            form = OauthAppForm()

            context = {
                "form": form,
            }

            return render(request, "upload/addOauthApp.html", context)


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
        return render(request, "upload/addOauthApp.html", context)
    else:
        if not OauthApp.objects.all().count():
            return redirect('upload:gettokens')
        # show new form to add new Oauth
        form = DeleteOauthAppForm()

        context = {
            "form": form,
        }

        return render(request, "upload/deleteOauthApp.html", context)
