from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest
from django.contrib.auth.decorators import login_required


# JASON RETURN
from django.http import JsonResponse
from django.core import serializers


from .models import Video

def index(request):
	context = {
		"title":"Index",
	}
	return render(request, "upload/index.html", context)

@login_required
def upload(request):

	if request.method == 'POST':
			videoname = request.POST.get('filename')
			if not videoname:
				return JsonResponse({"error":1},status=412)

			video_obj = Video.objects.create(name=videoname)
			video_obj_id = video_obj.id
			video_obj.save()
			# data_serialized = serializers.serialize("json", [video_obj.uuid])
			return JsonResponse({'uuid':video_obj.uuid},safe=False)

	# if not post show upload form 
	context = {
		"title":"Upload",
	}

	return render(request, "upload/upload.html", context)


	