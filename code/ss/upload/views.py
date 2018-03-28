from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from shutil import  move
import requests
import base64


@csrf_exempt
def upload(request):

	if request.method == 'POST':
		# check auth

		print( request.POST)
		move (request.POST["file.path"],"/upload/"+request.POST["file.name"])
		return HttpResponse("uploaded ")

	context = {
		"title":"Upload",
	}

	return render(request, "upload/upload.html", context)

@csrf_exempt
def gettokens(request):

	if request.method == 'POST':
		# check auth

		print( request.POST)
		return HttpResponse("gettokens post ")
	if request.method == 'GET' and request.GET.get('code'):
		post_data = {'code': request.GET["code"], 'redirect_uri': 'http://ss.dcm-ovs.com:8080/upload/gettokens/', 'grant_type': "authorization_code"}
		client_id = b'waEsgwg3NHj1sq1XsqTNEAcnjzenVON6Uto2O68k'
		client_secret =b'Z3w1EZLkH4DYAxOqJN7E5W3277f6c26S3KpYb6w4xp4q9BjBk5icjhOOIhSYCOAlNIfVICBA6ooIDdKuoZwXrHoJO7MSdsVYctKx1r9C1mFPUA1qwvdvIA5jPWFp7lgM' 
		bb64 = base64.b64encode(client_id + b":" + client_secret)
		bs = bb64.decode("utf-8")
		response = requests.post('http://web_dcm_ovs:8000/o/token/', data=post_data,headers={'Authorization': 'Basic '+ bs})
		
		if response:
			content = response.content
			# response content is json TODO parse it and store the acces and refresh tokens
			content = content.decode("utf-8")
			content = response.headers['Content-Type'] + content
		else:
			content="no response from server web"
	else:		
		content = '<a href="http://dcm-ovs.com/o/authorize/?client_id=waEsgwg3NHj1sq1XsqTNEAcnjzenVON6Uto2O68k&response_type=code&state=random_state_string">Authorize secure storage to access your account</a>'
	print(content)
	return HttpResponse( content)


	context = {
		"title":"gettokens",
	}

	return HttpResponse("gettokens ")
