from django.shortcuts import render
from django.http import HttpResponse
from .models import FbTemplate, EmailExample


def index(request):
    content = {
        'fb_templates': FbTemplate.objects.all().order_by('-pk')
    }
    return render(request,'fb_templates/index.html', content)


def view_template(request, tmp_id):
    temp = FbTemplate.objects.get(pk=tmp_id)
    return HttpResponse(temp.html)


def email_examples(request):
    emails_images = EmailExample.objects.all()
    content = {
        'emails_img': emails_images
    }
    return render(request, 'fb_templates/emails_examples.html', content)

