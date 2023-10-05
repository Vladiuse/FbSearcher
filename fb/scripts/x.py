from threading import Thread
import requests as req
from time import time
from accounts.models import FbAccount
from ads.models import FbGroup, FbPagExample
from django.core.paginator import Paginator
from parsers import FbGroupPage, FbGroupPageNoAuth
from proxies.models import Proxy
import os
import random as r
from time import sleep
from requests.exceptions import ConnectTimeout
from collections import Counter

groups = FbGroup.objects.exclude(email='')
unique = set()
counter = Counter()
for g in groups:
    mail, mail_domain = g.email.split('@')
    dom, last = mail_domain.split('.')
    counter[last]+=1

for i in counter.most_common():
    print(i)
# with open('/home/vlad/all.txt', 'w') as file:
#     for mail_domain in unique:
#         file.write(mail_domain + '\n')
