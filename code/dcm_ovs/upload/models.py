from django.db import models
import uuid

class Video(models.Model):
    #user   	  = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    name      = models.CharField(max_length=120, null=True, blank=True)
    # path      = models.TextField(blank=True, null=True)
    size      = models.BigIntegerField(default=0)
    file_type = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True) # first add can used to calculate uuid validation
    updated   = models.DateTimeField(auto_now=True) # mise a jour
    uploaded   = models.BooleanField(default=False)
    uuid      = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

