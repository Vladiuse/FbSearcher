from proxies.models import Proxy
from accounts.models import FbAccount
from ads.models import FbGroup
import requests as req
import os
from parsers import FbGroupPage
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pickle
from time import sleep
#
# proxy = Proxy.objects.get(pk=35)
# options = {
# 	'proxy': {
#         'https': proxy.url,
# 	}
# }
#
# driver = webdriver.Chrome( seleniumwire_options=options)
#
# groups = FbGroup.objects.filter(name="", email="")
# print(groups.count)
# driver.get('https:facebook.com/')
# cookies = pickle.load(open("cookies.pkl", "rb"))
# for cookie in cookies:
# 	driver.add_cookie(cookie)
# input('start: ')
# start = time.time()
# for num, group in enumerate(groups):
# 	driver.get(group.url)
# 	html = driver.page_source
# 	page = FbGroupPage(html)
# 	page()
# 	fbgroup_parse_res = page.result
# 	print(num,group, page.is_auth, fbgroup_parse_res)
# 	group.name = fbgroup_parse_res.get('group_name', '')
# 	group.email = fbgroup_parse_res.get('group_email', '')
# 	group.status = 'need_login'
# 	group.save()
# end = time.time()
# # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
# print(groups.count(), end- start, )
# print(groups.count()/ end- start)
# time.sleep(800)
#
# driver.quit()


account = FbAccount.objects.get(pk=12)
ext_path = '/home/vlad/html/cclelndahbckbenkjhflpdbgdldlbecc.zip'

chrome_options = Options()
chrome_options.add_extension(ext_path)
options = {
	'proxy': {
        'https': account.proxy.url,
	}
}

driver = webdriver.Chrome( seleniumwire_options=options, chrome_options=chrome_options)
driver.get('https://google.com/')
input()
driver.quit()
