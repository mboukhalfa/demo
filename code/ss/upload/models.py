from django.db import models

class OauthApp(models.Model):

    client_id = models.CharField(max_length=255, null=False, blank=False)
    client_secret = models.CharField(max_length=255, null=False, blank=False)
    redirect_uri = models.URLField(max_length=255, null=False, blank=False,help_text='Redirection URL',verbose_name='Redirection URL')
    timestamp = models.DateTimeField(auto_now_add=True) # first add can used to calculate uuid validation
    updated   = models.DateTimeField(auto_now=True) # mise a jour
    access_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)



