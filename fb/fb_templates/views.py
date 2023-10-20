from django.shortcuts import render
from django.http import HttpResponse
from .models import FbTemplate


def index(request):
    content = {
        'fb_templates': FbTemplate.objects.all()
    }
    return render(request,'fb_templates/index.html', content)

