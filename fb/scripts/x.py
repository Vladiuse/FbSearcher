from proxies.models import Proxy

from selenium import webdriver

proxy = Proxy.objects.get(pk=1)
chrome_options = webdriver.ChromeOptions()
print(proxy.url)
chrome_options.add_argument('--proxy-server=%s' % proxy.url)
browser = webdriver.Chrome(options=chrome_options)
browser.get('http://google.com/', )
input()