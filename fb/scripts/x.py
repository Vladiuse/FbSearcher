from proxies.models import Proxy
from accounts.models import FbAccount
from ads.models import FbGroup
import requests as req
import os
from parsers import FbGroupPage
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}
acc = FbAccount.objects.get(pk=6)

group = FbGroup.objects.get(pk="247331620535579")
res = req.get(
    'https://www.facebook.com/profile.php?id=247331620535579',
    headers=headers,
    cookies=acc.get_cookie(),
    proxies={'https': acc.proxy.url},
)
print(res.status_code)
page = FbGroupPage(res.text)
page()
print('page', page.is_auth, page.result)
group.log_req_data(res.text)
