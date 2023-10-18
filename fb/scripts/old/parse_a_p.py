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

LOG_PATH = '/home/vlad/log/'
groups = FbGroup.objects.all()
accounts = FbAccount.objects.select_related('proxy').all()


def task(account, page):
    requests_stats = []
    start = time()
    is_auth_count = 0
    for group in page.object_list:
        try:
            res = req.get(
                group.url,
                headers=account.HEADERS,
                proxies=account.proxy.url,
                cookies=account.get_cookie(),
                timeout=10,
            )
            if res.status_code == 200:
                fb_group_page = FbGroupPage(res.text)
                fb_group_page()
                group.update(fb_group_page.result)
                group.log_req_data(res.text)
                requests_stats.append([str(group), res.status_code, fb_group_page.is_auth])
                is_auth_count += fb_group_page.is_auth
            else:
                group.status = FbGroup.COLLECTED
                group.save()
                requests_stats.append([str(group), res.status_code, ])
        except ConnectTimeout as error:
            req_result = [str(group), 'ConnectTimeout', str(error)]
            requests_stats.append(req_result)
        except Exception as error:
            req_result = [str(group), 'Exception', str(error)]
            requests_stats.append(req_result)
    end = time()
    spend_time = round(end - start)
    total_groups = len(page.object_list)
    reqs_per_second = round(total_groups / spend_time)
    print(f'*** Page:{page} ***')
    print(
        f'Account: {account}, Time: {spend_time}, PerSec: {reqs_per_second},Groups:{total_groups}, AuthCount: {is_auth_count}')
    # log
    log_file_path = os.path.join(LOG_PATH, f'{account}.txt')
    with open(log_file_path, 'w') as log_file:
        for line in requests_stats:
            log_file.write(str(line) + '\n')


groups_per_page = round(len(groups) / len(accounts)) + 1
paginator = Paginator(groups, groups_per_page)

print('Groups: ', len(groups))
print('Acounts:', len(accounts))
print('Groups per Page: ', groups_per_page)
pairs = zip(accounts, [paginator.page(page_num) for page_num in paginator.page_range])
for pair in pairs:
    print(pair)
