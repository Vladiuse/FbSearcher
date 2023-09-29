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


res = req.get('https://www.facebook.com/profile.php?id=997341353721766')
print(res.status_code)
mail_domain = 'afdbayern.de'
page = FbGroupPage(res.text)
page()
print(page.result)
print(mail_domain in res.text)
with open('/home/vlad/html/test.html', 'w') as file:
    file.write(res.text)