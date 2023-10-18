from proxies.models import Proxy
from accounts.models import FbAccount
from ads.models import FbGroup
import requests as req
import os
from parsers import FbGroupPage
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import pickle
from time import sleep
import base64
import json


proxy = Proxy.objects.get(pk=35)
options = {
	'proxy': {
        'https': proxy.url,
	}
}

driver = webdriver.Chrome( seleniumwire_options=options)

groups = FbGroup.objects.filter(name="", email="")
print(groups.count)
driver.get('https:facebook.com/')
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
	driver.add_cookie(cookie)
input('start: ')
start = time.time()
for num, group in enumerate(groups):
	driver.get(group.url)
	html = driver.page_source
	page = FbGroupPage(html)
	page()
	fbgroup_parse_res = page.result
	print(num,group, page.is_auth, fbgroup_parse_res)
	group.name = fbgroup_parse_res.get('group_name', '')
	group.email = fbgroup_parse_res.get('group_email', '')
	group.status = 'need_login'
	group.save()
end = time.time()
# pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
print(groups.count(), end- start, )
print(groups.count()/ end- start)
time.sleep(800)

driver.quit()

account = FbAccount.objects.get(pk=11)
groups = FbGroup.objects.all()[:10]
ext_path = '/home/vlad/html/cclelndahbckbenkjhflpdbgdldlbecc.zip'

chrome_options = Options()
chrome_options.add_extension(ext_path)
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--ignore-certificate-errors')
options = {
    # 'proxy': {
    #     'https': account.proxy.url,
    # }
}
# cookie = '[{"domain":".facebook.com","hostOnly":false,"path":"\/","secure":true,"expirationDate":"1730381166","name":"sb","value":"WS0UZfwUKBVo3EIUZs0I7xbF"},{"domain":".facebook.com","hostOnly":false,"path":"\/","secure":true,"expirationDate":"1730381166","name":"datr","value":"WS0UZecvQTpSjfA1gKLTbrSM"},{"domain":".facebook.com","hostOnly":false,"path":"\/","secure":true,"expirationDate":"1727357166","name":"c_user","value":"100055990284401"},{"domain":".facebook.com","hostOnly":false,"path":"\/","secure":true,"expirationDate":"1727357166","name":"xs","value":"24%3ALjluSE9tXHN_fQ%3A2%3A1695821162%3A-1%3A-1"},{"domain":".facebook.com","hostOnly":false,"path":"\/","secure":true,"expirationDate":"1703597173","name":"fr","value":"0BwXYkn6wcDXaPmnj.AWU5m7xSO1EPGRCCCDBI3d8GQz8.BlFC1Z.LI.AAA.0.0.BlFC1v.AWUBEschD4g"},{"domain":".facebook.com","hostOnly":false,"path":"\/","secure":true,"expirationDate":"0","name":"presence","value":"C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1695821181332%2C%22v%22%3A1%7D"},{"domain":".facebook.com","hostOnly":false,"path":"\/","secure":true,"expirationDate":"1696425997","name":"wd","value":"901x905"}]'
# cookie = json.loads(cookie)
driver = webdriver.Chrome(seleniumwire_options=options, chrome_options=chrome_options)
driver.set_page_load_timeout(5)
start = time.time()
for num,group in enumerate(groups):
    try:
        driver.get(group.url)
        html = driver.page_source
        page = FbGroupPage(html)
        page()
        fbgroup_parse_res = page.result
        print(num,group, page.is_auth, fbgroup_parse_res)
        group.name = fbgroup_parse_res.get('group_name', '')
        group.email = fbgroup_parse_res.get('group_email', '')
        group.status = 'need_login'
        group.save()
        group.log_req_data(html)
    except TimeoutException as error:
        print(group,error)
end = time.time()
print(end - start)
print(end - start / groups.count())
input('Press enter to exit: ')
driver.quit()
