from threading import Thread
import requests as req
from time import time
from accounts.models import FbAccount
from ads.models import FbGroup
from django.core.paginator import Paginator
accounts = FbAccount.work_objects.select_related('proxy').all()
fb_groups = FbGroup.objects.filter(status=FbGroup.NOT_LOADED)
from parsers import FbGroupPage
import os
import random as r
from time import sleep
from requests.exceptions import ConnectionError
def time_sleep_factory(max,min):
    def go_sleep():
        to_sleep = r.uniform(max, min)
        sleep(to_sleep)
    return go_sleep

PATH_SAVE_HTML = '/home/vlad/PycharmProjects/FbSearcher/fb/media/req_html_data'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

before_req_sleep = time_sleep_factory(0.5, 1.5)
def task(account, page):
    sleep(3)
    print('\n***** STREAM *****', account, page)
    start = time()
    fbgroups_pages_is_auth = []
    stat = []
    for fb_group in page.object_list:
        before_req_sleep()
        try:
            res = req.get(fb_group.url,
                          headers=headers,
                          cookies=account.get_cookie(),
                          proxies={'https': account.proxy.url},
                          )
            if res.status_code == 200:
                fbgroup_page = FbGroupPage(res.text)
                fbgroup_page()
                fbgroups_pages_is_auth.append(fbgroup_page.is_auth)
                fbgroup_parse_res = fbgroup_page.result
                fb_group.name = fbgroup_parse_res.get('group_name', '')
                fb_group.email = fbgroup_parse_res.get('group_email', '')
                fb_group.status = FbGroup.COLLECTED
                stat.append([str(fb_group), res.status_code, fbgroup_page.is_auth])
            else:
                stat.append([str(fb_group), res.status_code, ])
            fb_group.save()
        except ConnectionError as error:
            stat.append([str(fb_group), str(error), ])
    end = time()
    group_count = len(page.object_list)
    print( '****** END ****** ',account,)
    total_time = round(end - start, 1)
    auth_count_true = fbgroups_pages_is_auth.count(True)
    auth_count_false = fbgroups_pages_is_auth.count(False)
    per_seccond = round(group_count / total_time, 1)
    print(f'Total time: {total_time}, Per sec: {per_seccond}, auth_count: {auth_count_true}/{auth_count_false}')
    with open(f'/home/vlad/html/{str(account)}.txt', 'w') as file:
        for line in stat:
            file.write(str(line)+'\n')

groups_per_page = round(fb_groups.count() / accounts.count()) + 2
print('Groups to pars', fb_groups.count())
print('Accounts', accounts.count())
print('groups_per_page', groups_per_page)
paginator = Paginator(fb_groups, groups_per_page)
pairs = zip(accounts, paginator.page_range)
for account, page_num in pairs:
    page = paginator.page(page_num)
    print(account,page)
    thread = Thread(target=task, args=[account, page,])
    thread.start()



