from threading import Thread
import requests as req
from time import time
from accounts.models import FbAccount
from ads.models import FbGroup
from django.core.paginator import Paginator
from parsers import FbGroupPage
from proxies.models import Proxy
import os
import random as r
from time import sleep
from requests.exceptions import ConnectTimeout

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

proxy = Proxy.objects.get(pk=89)
start = time()
def task(page):
    for num,group in enumerate(page.object_list):
        try:
            res = req.get(group.url, headers=HEADERS, timeout=6, proxies={'https': proxy.url})
            if res.status_code == 200:
                page = FbGroupPage(res.text)
                page()
                group.update(page.result)
                group.log_req_data(res.text)
                print(num,group,'\n', page.result,)
        except TimeoutError as error:
            print(group,'\n',  error)
        except Exception as error:
            print(group,'\n',  error)

end = time()
print(start- end)
groups = FbGroup.objects.filter(status='not_loaded')
print(groups.count())
paginator = Paginator(groups, 710)
for page_num in paginator.page_range:
    page = paginator.page(page_num)
    print(page)
    thread = Thread(target=task, args=[page,])
    thread.start()




