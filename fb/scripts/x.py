import requests as req
from accounts.models import FbAccount
from bs4 import BeautifulSoup
from os import path
FB_MAIN_URL = 'https://facebook.com/'

vlad = FbAccount.objects.get(name='vlad')
dir_path = '/home/vlad/PycharmProjects/FbSearcher/fb/parsers/fb_pages_html/group_page/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}
FB_GROUP_URL = 'https://facebook.com/pattrnsocial/'
res = req.get(FB_GROUP_URL, headers=headers)
print(res.status_code)
path_to_save = path.join(dir_path, 'group_no_login.html')
with open(path_to_save, 'w') as file:
    file.write(res.text)




