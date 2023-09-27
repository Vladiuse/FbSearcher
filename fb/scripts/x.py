from threading import Thread
import requests as req
from time import time
from accounts.models import FbAccount
from ads.models import FbGroup
from django.core.paginator import Paginator
from parsers import FbGroupPage
from proxies.models import Proxy
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

account = FbAccount.objects.get(pk=12)
group = FbGroup.objects.get(pk='177855115588808')
proxies = Proxy.objects.filter(pk__in=range(75,81))
for proxi in proxies:
    res = req.get('https://facebook.com/',
                  headers=headers,
                  proxies={'https':account.proxy.url},
                  cookies=account.get_cookie(),
                  )
    print(res.status_code, 'The Week UK' in res.text)
    page = FbGroupPage(res.text)
    page()
    print('Page is auth',page.is_auth)

# with open(group.req_html_data.path) as file:
#     html = file.read()
#
# page = FbGroupPage(html)
# page()
# print(page.is_auth)
# # group.log_req_data(html)
#
#
# soup = BeautifulSoup(html, 'lxml')
# print(soup.text)