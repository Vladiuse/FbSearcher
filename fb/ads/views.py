from rest_framework.views import APIView
from django.shortcuts import render
from .serializers import FbGroupCreateSerializer
from rest_framework.response import Response
from .forms import FbLibCsvForm
import csv
from django.http import HttpResponse

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


class FbLibStatCsvReader:

    def __init__(self, path):
        self.path = path
        self.group_ids = set()
        self.total = 0

    def __call__(self):
        with open(self.path, 'r', encoding='utf-8') as csv_file:
            table = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            for row in table:
                self.group_ids.add(row['page_id'])
                self.total += 1

    def __len__(self):
        return len(self.group_ids)

def update_from_csv(request):
    if request.method == 'POST':
        form = FbLibCsvForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['csv_file']
            fb_lib_file_reader = FbLibStatCsvReader(file.temporary_file_path())
            fb_lib_file_reader()
            res = str(len(fb_lib_file_reader))
            return HttpResponse(res)
        else:
            content = {
                'form': form,
            }
            return render(request, 'ads/fb_ads_load_csv.html', context=content)
    else:
        form = FbLibCsvForm()
        content = {
            'form': form,
        }
        return render(request,'ads/fb_ads_load_csv.html', context=content)
