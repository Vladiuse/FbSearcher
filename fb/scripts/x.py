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


fb_group = FbPagExample.objects.get(pk=5)
with open(fb_group.template.path) as file:
    html = file.read()

page = FbGroupPageNoAuth(html)
print(page._get_name_from_code())