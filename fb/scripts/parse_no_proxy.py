from threading import Thread
import requests as req
from time import time
from accounts.models import FbAccount
from ads.models import FbGroup
from django.core.paginator import Paginator
from parsers import FbGroupPage
import os
import random as r
from time import sleep
from requests.exceptions import ConnectTimeout

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

group = FbGroup.objects.all()[1251:]
start = time()
for num,group in enumerate(group):
    try:
        res = req.get(group.url, headers=HEADERS, timeout=6)
        if res.status_code == 200:
            page = FbGroupPage(res.text)
            page()
            group.update(page.result)
            group.log_req_data(res.text)
            print(num,group, page.result,)
    except TimeoutError as error:
        print(group, error)
    except Exception as error:
        print(group, error)

end = time()
print(start- end)







