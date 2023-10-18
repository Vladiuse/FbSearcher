import random as r
from time import sleep, time
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from .serializers import FbGroupCreateSerializer
from rest_framework.response import Response
from .forms import FbLibCsvForm, FbLibZipForm, TxtFileForm
from .fb_adlib_csv_reader import FbLibStatCsvReader, FbLibStatZipReader, Fb7DaysZipReader, TxtFileReader
from .models import FbGroup, KeyWord
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ThreadCounter
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Count


def index(request):
    return render(request, 'ads/index.html')


class FbGroupUpdateOrCreateView(APIView):

    def post(self, request):
        groups_items = request.data['group_urls']
        print(groups_items)
        invalid_data = []
        invalid_count = 0
        total = len(groups_items)
        new = 0
        for item in groups_items:
            serializer = FbGroupCreateSerializer(data=item)
            if serializer.is_valid():
                group, created = serializer.save()
                if created:
                    new += 1
            else:
                invalid_count += 1
                invalid_data.append(item)
        response = {
            'invalid_data': invalid_data,
            'invalid_count': invalid_count,
            'total': total,
            'new': new,
        }
        return Response(response)


class UpdateFbGroupFromCsv(View):
    """Обновить БД фб групп из csv"""
    template_name = 'ads/fb_ads_load_csv.html'

    def get(self, request):
        form = FbLibCsvForm()
        content = {
            'form': form,
        }
        return render(request, self.template_name, context=content)

    def post(self, request):
        form = FbLibCsvForm(request.POST, request.FILES)
        if form.is_valid():
            start_groups_count = FbGroup.objects.count()
            files = request.FILES.getlist('csv_file')
            readers_n_results = []
            for file in files:
                fb_lib_file_reader = FbLibStatCsvReader(file.temporary_file_path(), file_name=file.name)
                fb_lib_file_reader.read()
                update_result = FbGroup.update_db_by_group_ids(fb_lib_file_reader)
                readers_n_results.append([fb_lib_file_reader,update_result])
            content = {
                'form': FbLibCsvForm(),
                'readers_n_results': readers_n_results,
                'total_result': None,
                'new_groups_created': FbGroup.objects.count() - start_groups_count,
            }
            return render(request, self.template_name, context=content)
        else:
            content = {
                'form': form,
            }
            return render(request, self.template_name, context=content)

    def read_one_csv_file(self):

        pass

    def read_few_csv_files(self):
        pass


class UpdateFbGroupFromZip(View):
    """Обновить БД фб групп из zip"""
    template_name = 'ads/zip_load/index.html'


    def get(self, request):
        form = FbLibZipForm()
        content = {
            'form': form,
        }
        return render(request, self.template_name, context=content)

    def post(self, request):
        form = FbLibZipForm(request.POST, request.FILES)
        if form.is_valid():
            print('VALID')
            csv_file_type = form.cleaned_data['zip_file_type']
            if csv_file_type == FbLibZipForm.FB_ADS_LIB_TYPE:
                reader_class = FbLibStatZipReader
            else:
                reader_class = Fb7DaysZipReader
            start_groups_count = FbGroup.objects.count()
            readers_n_results = []
            files = request.FILES.getlist('zip_files')
            for file in files:
                if isinstance(file, InMemoryUploadedFile):
                    reader = reader_class(file, file_name=file.name, add_low_spend=form.cleaned_data['add_low_spend'])
                else:
                    reader = reader_class(file.temporary_file_path(), file_name=file.name, add_low_spend=form.cleaned_data['add_low_spend'])
                reader.read()
                update_result = FbGroup.update_db_by_group_ids(reader)
                readers_n_results.append([reader,update_result])
            content = {
                'form': FbLibZipForm(),
                'readers_n_results': readers_n_results,
                'total_result': None,  # TODO remove??
                'new_groups_created': FbGroup.objects.count() - start_groups_count,
            }
            return render(request, self.template_name, context=content)
        else:
            content = {
                'form': form,
            }
            return render(request, self.template_name, context=content)


class UpdateFbGroupFromTxt(View):
    """Обновить БД фб групп из txt"""

    template_name = 'ads/txt_load/index.html'

    def get(self, request):
        form = TxtFileForm()
        content = {
            'form': form,
        }
        return render(request, self.template_name, content)

    def post(self, request):
        print(request.POST)
        form = TxtFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('txt_files')
            reader_class = TxtFileReader
            start_groups_count = FbGroup.objects.count()
            readers_n_results = []
            for file in files:
                if isinstance(file, InMemoryUploadedFile):
                    reader = reader_class(file, file_name=file.name,)
                else:
                    reader = reader_class(file.temporary_file_path(), file_name=file.name,)
                reader.read()
                #update_result = FbGroup.update_db_by_group_ids(reader)
                update_result = {
                    'new': 10,
                    'updated': 100,
                }
                readers_n_results.append([reader,update_result])
            content = {
                'form': TxtFileForm(),
                'readers_n_results': readers_n_results,
                'total_result': None, # TODO remove??
                'new_groups_created': FbGroup.objects.count() - start_groups_count,
            }
            return render(request, self.template_name, context=content)

        else:
            print(form.errors)
            content = {
                'form': form,
            }
            return render(request, self.template_name, context=content)

def groups_stat(request):
    content = {
        'not_collected_count': FbGroup.not_collected_objects.count(),
        'collected_count': FbGroup.collected_objects.count(),
        'error_req_count': FbGroup.error_req_objects.count(),
        'with_mail_count': FbGroup.full_objects.count(),
        'no_mail_count': FbGroup.collected_no_mail_objects.count(),
        'no_data_count': FbGroup.collected_no_data_objects.count(),
        'login_form_count': FbGroup.collected_objects.filter(name='FaceBook').count(),
        'mails_service_stat': FbGroup.full_objects.values('email_service').annotate(count=Count('*')).order_by('email_service')
    }
    return render(request, 'ads/groups_stat.html', content)

def download_page(request):
    content = {
        'with_mail_count': FbGroup.full_objects.count(),
        'ignored_services_group': FbGroup.objects.select_related('email_service').filter(email_service__ignore=True),
        'ignored_by_name': FbGroup.ignored_by_name(),
    }
    return render(request, 'ads/download_page.html', content)

def mark_mail_services(request):
    FbGroup.mark_mail_services()
    return redirect('groups_stat')

def key_words(request):
    key_words = KeyWord.objects.all()
    content = {'key_words': key_words}
    return render(request, 'ads/key_words.html', content)


def load_actual_mails(request):
    path = FbGroup.create_file()
    with open(path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="text/csv")
        return response

@csrf_exempt
def sleep_10(request):
    try:
        name = request.POST['name']
        model, created = ThreadCounter.objects.get_or_create(name=name)
        model.count += 1
        model.save()
        return HttpResponse(f'{model} {model.count}')
    except Exception as error:
        return HttpResponse(str(error))
