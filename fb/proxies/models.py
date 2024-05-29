from datetime import datetime
from time import sleep
from django.db import models
from .check_proxies import get_current_ip, check_proxy, get_proxy_ip, CheckerNotWorkError, ProxyIpNotChange, CodeNot200
from requests.exceptions import ConnectTimeout, RequestException, ProxyError, Timeout
from threading import Thread
import requests as req
import time

class ProxyChangeIpUrlNotWork(Exception):
    """Proxy url for change ip not work"""
class ProxyChangeIpTimeOutError(Exception):
    pass

class ProxyAbs(models.Model):
    WORK = True
    NOT_WORK = False
    NOT_CHECKED = None
    STATUSES = (
        (WORK, 'Работает'),
        (NOT_WORK, 'Не работает'),
        (NOT_CHECKED, 'Не проверен'),
    )
    HTTP = 'http'
    HTTPS = 'https'
    SOCKS5 = 'socks5'
    PROTOCOLS = (
        (HTTP, HTTP),
        (HTTPS, HTTPS),
        (SOCKS5, SOCKS5),
    )
    ip = models.CharField(max_length=30, verbose_name='ip/host')
    port = models.CharField(max_length=6)
    status = models.BooleanField(max_length=50, default=NOT_CHECKED, null=True)
    protocol = models.CharField(max_length=10, choices=PROTOCOLS, default=HTTP)
    created = models.DateField(auto_now_add=True)
    comment = models.CharField(max_length=255, blank=True, )
    proxy_ip = models.CharField(max_length=20,blank=True)
    error_type = models.CharField(max_length=50, blank=True)
    error_text_full = models.TextField(blank=True)

    class Meta:
        abstract = True
        unique_together = ['ip', 'port']

    def __str__(self):
        return f'{self.pk}: {self.comment}'

    @property
    def url(self):
        return f'{self.protocol}://{self.ip}:{self.port}/'

    def check_proxy(self):
        self.status = self.NOT_CHECKED
        try:
            proxy_ip = check_proxy(self.url)
            self.proxy_ip = proxy_ip
            self.status = self.WORK
            self.error_type = ''
            self.error_text_full = ''
        except CheckerNotWorkError as error:
            self.error_type = 'CheckerNotWorkError'
            self.error_text_full = 'Checkers not work'
        except ProxyIpNotChange as error:
            self.error_type = 'ProxyIpNotChange'
            self.error_text_full = str(error)
            self.status = self.NOT_WORK
        except (Timeout, ProxyError, RequestException) as error:
            self.error_type = type(error).__name__
            self.status = self.NOT_WORK
            self.error_text_full = str(error)
        self.save()

    @staticmethod
    def check_proxies(qs):
        for proxy_model in qs:
            proxy_model.check_proxy()

    @property
    def current_ip(self):
        return get_proxy_ip(self.url)

class Proxy(ProxyAbs):
    pass

class ProxyAuth(ProxyAbs):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    @property
    def url(self):
        return f'{self.protocol}://{self.login}:{self.password}@{self.ip}:{self.port}/'

class ProxyMobile(ProxyAbs):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    change_ip_url = models.URLField()

    @property
    def url(self):
        return f'{self.protocol}://{self.login}:{self.password}@{self.ip}:{self.port}/'


    @property
    def change_ip_url_json(self):
        return f'{self.change_ip_url}&format=json'

    def quik_change_ip(self):
        for try_num in range(3):
            print(f'try #{try_num + 1} change proxy ip: p{self.pk}', datetime.today().time())
            try:
                res = req.get(self.change_ip_url_json, timeout=90)
                if res.status_code != 200:
                    print('Cant change ip status code not 200')
                    print(res.text)
                else:
                    res_data = res.json()
                    print(f'p{self.pk}',res_data,)
                    if res_data['status'] == 'OK':
                        return
                    if res_data['message'] == 'Already change IP, please wait':
                        return
            except RequestException as error:
                print('Cant change ip', type(error))
        raise ProxyChangeIpUrlNotWork

    def _click_change_ip_url(self):
        """Перейти по ссылки для сменны ip прокси"""
        try:
            res = req.get(self.change_ip_url, timeout=50)
            if res.status_code != 200:
                raise CodeNot200
        except (RequestException, CodeNot200) as error:
            raise ProxyChangeIpUrlNotWork(str(error))

    def change_ip(self):
        no_proxy_ip = get_current_ip()
        old_proxy_ip = get_proxy_ip(self.url)
        print('\nСмена IP')
        print('Без прокси: ', no_proxy_ip)
        print('Tекущий: ', old_proxy_ip)
        self._click_change_ip_url()
        new_proxy_ip = 'не получен'
        for _ in range(5):
            try:
                new_proxy_ip = get_proxy_ip(self.url)
                if new_proxy_ip != old_proxy_ip and new_proxy_ip != no_proxy_ip:
                    print('Новый: ', new_proxy_ip)
                    return new_proxy_ip
            except CheckerNotWorkError as error:
                pass
            time.sleep(5)
        raise ProxyChangeIpTimeOutError(no_proxy_ip, old_proxy_ip,new_proxy_ip)

    def test_sleep(self):
        time.sleep(100)

    @staticmethod
    def print_for_config():
        proxies =  ProxyMobile.objects.all()
        print('[Proxy]')
        for proxy in proxies:
            print(f'p{proxy.pk} = {proxy.url}')
        print('')
        print('[ProxyChangeIpUrl]')
        for proxy in proxies:
            print(f'p{proxy.pk} = {proxy.change_ip_url}&format=json')