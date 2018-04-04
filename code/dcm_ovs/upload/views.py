from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# JASON RETURN
from django.http import JsonResponse

from .models import Video


def index(request):
    context = {
        "title": "Index",
    }
    return render(request, "upload/index.html", context)


@login_required
def upload(request):
    if request.method == 'POST':
        video_name = request.POST.get('filename')
        if not video_name:
            return JsonResponse({"error": 1}, status=412)

        video_obj = Video.objects.create(name=video_name)
        video_obj.save()
        return JsonResponse({'uuid': video_obj.uuid}, safe=False)

    # if not post show upload form
    context = {
        "title": "Upload",
    }

    return render(request, "upload/upload.html", context)
