from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    content = {}
    return render(request,'fb_templates/index.html', content)

