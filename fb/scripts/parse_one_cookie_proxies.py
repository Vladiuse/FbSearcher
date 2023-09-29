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

group = FbGroup.objects.all()

account = FbAccount.objects.get(pk=4)
proxies = Proxy.objects.exclude(pk=2)
jar = account.get_cookie()
def task(proxy,page):
    start = time()
    count = 0
    for num,group in enumerate(page.object_list):
        try:
            res = req.get(group.url,
                          headers=HEADERS,
                          timeout=7,
                          cookies=jar,
                          proxies={'https':proxy.url},
                          )
            if res.status_code == 200:
                fb_page = FbGroupPage(res.text)
                fb_page()
                res = fb_page.result
                if 'group_email' in res:
                    group.update(res)
                    count += 1
        except TimeoutError as error:
            with open('/home/vlad/html/errors.txt', 'a') as file:
                file.write(str(error)+'\n')
            pass
        except Exception as error:
            with open('/home/vlad/html/errors.txt', 'a') as file:
                file.write(str(error) + '\n')
            pass
    end = time()
    print(page,proxy,'collected: ', count, 'Time: ',end - start)


groups = FbGroup.objects.all()
print(groups.count())
per_page = round(groups.count() / proxies.count()) + 1
print('Per page', per_page)
paginator = Paginator(groups, per_page)
pairs = zip(proxies, [paginator.page(page_num) for page_num in paginator.page_range])
for proxy, page in pairs:
    print(proxy, page)

    thread = Thread(target=task, args=[proxy,page,])
    thread.start()






