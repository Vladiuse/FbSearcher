from django.shortcuts import render
from django.http import HttpResponse
from .models import FbTemplate


def index(request):
    content = {
        'fb_templates': FbTemplate.objects.all()
    }
    return render(request,'fb_templates/index.html', content)


def view_template(request, tmp_id):
    temp = FbTemplate.objects.get(pk=tmp_id)
    return HttpResponse(temp.html)

