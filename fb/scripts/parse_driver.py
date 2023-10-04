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



url = 'https://www.facebook.com/profile.php?id=997341353721766'
groups = FbGroup.objects.all()[:100]
driver = webdriver.Chrome()
driver.get(url)
for group in groups:
    driver.get(url)
driver.get(url)

source = driver.page_source
innerHTML = driver.execute_script("return document.body.innerHTML")

page_sorce = FbGroupPage(source)
innerHTML_page = FbGroupPage(innerHTML)
with open('/home/vlad/html/source.html', 'w') as file:
    file.write(source)

with open('/home/vlad/html/inner.html', 'w') as file:
    file.write(innerHTML)

page_sorce()
innerHTML_page()

print(page_sorce.result)
print(innerHTML_page.result)

print('afdbayern.de' in source)
print('afdbayern.de' in innerHTML)

sleep(5)
print('\n*********************')
source = driver.page_source
innerHTML = driver.execute_script("return document.body.innerHTML")

page_sorce = FbGroupPage(source)
innerHTML_page = FbGroupPage(innerHTML)
with open('/home/vlad/html/source_sleep.html', 'w') as file:
    file.write(source)

with open('/home/vlad/html/inner_sleep.html', 'w') as file:
    file.write(innerHTML)
print('afdbayern.de' in source)
print('afdbayern.de' in innerHTML)

input()
driver.quit()