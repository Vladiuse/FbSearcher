import requests as req
from accounts.models import FbAccount
FB_MAIN_URL = 'https://facebook.com/'

vlad = FbAccount.objects.get(name='vlad')

res = req.get(FB_MAIN_URL, cookies=vlad.get_cookie())
print(res.status_code)
with open('parsers/fb_pages_html/fb_main_login.html', 'w') as file:
    file.write(res.text)