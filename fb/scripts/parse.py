from threading import Thread
import requests as req
from time import time
from accounts.models import FbAccount
from ads.models import FbGroup
from django.core.paginator import Paginator
accounts = FbAccount.objects.select_related('proxy').all()
fb_groups = FbGroup.objects.all()
from parsers import FbGroupPage
import os

PATH_SAVE_HTML = '/home/vlad/PycharmProjects/FbSearcher/fb/media/req_html_data'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}
def task(account, page):
    print('\n***** STREAM *****', account, page)
    start = time()
    fbgroups_pages_is_auth = []
    for fb_group in page.object_list:
        res = req.get(fb_group.url,
                      headers=headers,
                      cookies=account.get_cookie(),
                      proxies={'https': account.proxy.url},
                      )
        #log
        # file_name = f'{fb_group.pk}_{res.status_code}.html'
        # path_to_save = os.path.join(PATH_SAVE_HTML, file_name)
        # #log

        fbgroup_page = FbGroupPage(res.text)
        fbgroup_page()
        fbgroups_pages_is_auth.append(fbgroup_page.is_auth)
        fbgroup_parse_res = fbgroup_page.result
        fb_group.name = fbgroup_parse_res.get('group_name', '')
        fb_group.email = fbgroup_parse_res.get('group_email', '')
        fb_group.save()
    end = time()
    group_count = len(page.object_list)
    print( '****** END ****** ',account,)
    total_time = round(end - start, 1)
    auth_count = fbgroups_pages_is_auth.count(True)
    per_seccond = round(group_count / total_time, 1)
    print(f'Total time: {total_time}, Per sec: {per_seccond}, auth_count: {auth_count}')


paginator = Paginator(fb_groups, 100)
pairs = zip(accounts, paginator.page_range)
for account, page_num in pairs:
    page = paginator.page(page_num)
    print(account,page)
    thread = Thread(target=task, args=[account, page,])
    thread.start()



