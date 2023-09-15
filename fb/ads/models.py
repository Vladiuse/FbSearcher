from django.db import models

def clean_fb_group_url(url):
    pass



class FbGroup(models.Model):

    GROUP_DOMAIN = 'facebook.com'

    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255,blank=True)
    raw_url = models.URLField()