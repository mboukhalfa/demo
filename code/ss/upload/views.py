from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from django.views.decorators.csrf import csrf_exempt

from shutil import move
from django.utils.timezone import utc
from django.utils.dateparse import parse_datetime

import datetime
import requests
from oauth.models import OauthApp

from .validator.validator import VideoValidator
from django.conf import settings
'''
 SETTINGS
	  '''
UUID_EXPIRE_SECONDS = settings.UUID_EXPIRE_SECONDS
WEB_SERVER_URL_ROOT = settings.WEB_SERVER_URL_ROOT
WEB_SERVER_URL_API_UPLOAD = settings.WEB_SERVER_URL_API_UPLOAD


@csrf_exempt
def auth(request):
    # ignore options request method
    if request.META['HTTP_X_ORIGINAL_METHOD'] == 'OPTIONS':
        return HttpResponse("good")

    try:
        uuid = request.META['HTTP_UUID']
    except:
        return HttpResponse("no uuid", status=401)

    for i in range(1, 3):

        if OauthApp.objects.all().count():
            oauthAppObject = OauthApp.objects.all().first()
            if not oauthAppObject.access_token:
                return HttpResponse("no access token ", status=403)
        else:
            raise PermissionDenied

        # check if uuid is valid
        response = requests.get(WEB_SERVER_URL_ROOT + WEB_SERVER_URL_API_UPLOAD + uuid + '/',
                                headers={'Authorization': 'Bearer ' + oauthAppObject.access_token})

        if response:
            # if valide time and not uploaded
            json_data = response.json()
            timediff = datetime.datetime.utcnow().replace(tzinfo=utc) - parse_datetime(json_data['timestamp'])
            if json_data['uploaded'] or timediff.total_seconds() > UUID_EXPIRE_SECONDS:
                raise PermissionDenied  # maybe we can inform that this uuid not valid
            else:
                # validate and oauth video in oauth view
                return HttpResponse("good")

        #  else maybe because of access token or UUID non valide
        else:
            # if uuid not valide
            if response.status_code == requests.codes['not_found']:
                raise PermissionDenied

            # refresh access token
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


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        # validate video
        v_v = VideoValidator(request.POST)
        if not v_v.is_valid():
            return HttpResponse("Unsupported Media Type", status=415)

        # inform website that video uploaded
        if OauthApp.objects.all().count():
            oauthAppObject = OauthApp.objects.all().first()
            if not oauthAppObject.access_token:
                return HttpResponse("no access token ", status=403)
        else:
            raise PermissionDenied
        uuid = request.META['HTTP_UUID']
        r = requests.put(WEB_SERVER_URL_ROOT + WEB_SERVER_URL_API_UPLOAD + uuid + '/',
                         headers={'Authorization': 'Bearer ' + oauthAppObject.access_token},
                         data={'uploaded': True})

        if r:
            # from mime type in VideoValidator we can find ext than rename file
            move(request.POST["file.path"], "/upload/" + request.POST["file.name"])
            return HttpResponse("uploaded ")

        else:
            return HttpResponse("unable confirm oauth", status=504)

    return HttpResponse("no response from server web ", status=444)

