from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from shutil import  move


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



