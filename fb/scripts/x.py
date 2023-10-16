from threading import Thread
import requests as req
from time import time
from accounts.models import FbAccount
from ads.models import FbGroup, FbPagExample, MailService, KeyWord
from django.core.paginator import Paginator
from parsers import FbGroupPage, FbGroupPageNoAuth
from proxies.models import Proxy
import os
import random as r
from time import sleep
from requests.exceptions import ConnectTimeout
from collections import Counter
import re
from django.db.models import Count
from collections import Counter
from django.db.models.functions import Length
from parsers.fb_ads_lib_parser import FbLibPage
from datetime import datetime, timedelta
# with open('scripts/load_data.txt') as file:
#     for line in file:
#         try:
#             KeyWord.objects.create(
#                 word=line.strip()
#             )
#         except:
#             pass



q = 'food'
days_ago = 1
start_date = str(datetime.now().date() - timedelta(days=days_ago))
country = 'US'
url = f'https://www.facebook.com/ads/library/?active_status=active&ad_type=political_and_issue_ads&country={country}&q={q}&publisher_platforms[0]=facebook&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&start_date[min]={start_date}&start_date[max]=&search_type=keyword_unordered&media_type=all'

print(url)
keys = KeyWord.objects.filter(ads_count_all__isnull=True).order_by(Length('word').asc())
# keys = KeyWord.objects.filter(ads_count_all__isnull=True)
page = FbLibPage(q='', start_date=start_date, country=country)
for q in keys:
    try:
        page.q = q
        page.open()
        print(q, page._get_count_of_adds())
        if page._get_count_of_adds():
            q.ads_count_policy = page._get_count_of_adds()
            q.save()
    except Exception as error:
        print(error)

