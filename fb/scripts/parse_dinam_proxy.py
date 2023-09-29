from threading import Thread
import requests as req
from time import time
from accounts.models import FbAccount
from ads.models import FbGroup
from django.core.paginator import Paginator
accounts = FbAccount.work_objects.select_related('proxy').filter(pk__in=[10,11,12])
fb_groups = FbGroup.objects.filter(status=FbGroup.NOT_LOADED)
from parsers import FbGroupPage


url = 'https://api64.ipify.org?format=json'
res = req.get(url, proxies={
    'http': 'http://marikmaison200:gwRqDBwRp3@78.46.100.233:42267/',
    'https': 'http://marikmaison200:gwRqDBwRp3@78.46.100.233:42267/',
})
print(res.status_code)
print(res.text)