import random as r
from time import sleep, time
from rest_framework.views import APIView
from django.shortcuts import render
from .serializers import FbGroupCreateSerializer
from rest_framework.response import Response
from .forms import FbLibCsvForm, FbLibZipForm
from .fb_adlib_csv_reader import FbLibStatCsvReader, FbLibStatZipReader, Fb7DaysZipReader
from .models import FbGroup
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ThreadCounter
from django.core.files.uploadedfile import InMemoryUploadedFile



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
        print(request.POST)
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
                    reader = reader_class(file, file_name=file.name)
                else:
                    reader = reader_class(file.temporary_file_path(), file_name=file.name)
                reader.read()
                update_result = FbGroup.update_db_by_group_ids(reader)
                readers_n_results.append([reader,update_result])
            content = {
                'form': FbLibZipForm(),
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

def groups_stat(request):
    content = {
        'not_collected_count': FbGroup.not_collected_objects.count(),
        'collected_count': FbGroup.collected_objects.count(),
        'error_req_count': FbGroup.error_req_objects.count(),
        'with_mail_count': FbGroup.full_objects.count(),
        'no_mail_count': FbGroup.collected_no_mail_objects.count(),
        'no_data_count': FbGroup.collected_no_data_objects.count(),
        'login_form_count': FbGroup.collected_objects.filter(name='FaceBook').count()
    }
    return render(request, 'ads/groups_stat.html', content)

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
