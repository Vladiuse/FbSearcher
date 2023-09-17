from ads.models import FbGroup, clean_fb_group_url, replace_http
from ads.serializers import FbGroupSerializer , FbLibAdCreateSerializer

FbGroup.objects.all().delete()
data = {'group_url': 'https://facebook.com/123/',
        'id': '859762788802222',
        'name': 'All Language Translator',
        'time_text': 'Показ начат 23 ноя 2022 г.',
        'status': 'Активно',
        }

url = 'https://x.facebook.com/1235'
url = replace_http(url)
id = clean_fb_group_url(url)
# group = FbGroup(id=id, raw_url=url)
# group.full_clean()
# group.save()
group, created = FbGroup.objects.create_or_update(id=id, raw_url=url)
print(group.pk, group.url)

[{'group_url': 'https://facebook.com/123/'},{'group_url': 'https://facebook.com/1/'},{'group_url': 'https://facebook.com/2/'}]