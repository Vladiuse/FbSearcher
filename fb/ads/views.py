from time import sleep
from rest_framework.views import APIView
from django.shortcuts import render
from .serializers import FbGroupCreateSerializer
from rest_framework.response import Response
from .forms import FbLibCsvForm
from .fb_adlib_csv_reader import FbLibStatCsvReader
from .models import FbGroup
from django.views import View
from django.http import HttpResponse


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
    template_name = 'ads/fb_ads_load_csv.html'

    def get(self, request):
        form = FbLibCsvForm()
        content = {
            'form': form,
        }
        return render(request, self.template_name, context=content)

    def post(self, request):
        sleep(5)
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
