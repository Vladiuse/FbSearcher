from django.db import models
from .check_proxies import CheckProxyApi64, CheckProxyHttpBin, CodeNot200
from requests.exceptions import ConnectTimeout

class Proxy(models.Model):
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
    ip = models.GenericIPAddressField()
    port = models.CharField(max_length=6)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    status = models.BooleanField(max_length=50,  default=NOT_CHECKED, null=True)
    error_text = models.CharField(max_length=255, blank=True)
    protocol = models.CharField(max_length=10, choices=PROTOCOLS, default=HTTP)
    created = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['ip', 'port']

    def __str__(self):
        return f'Id:{self.pk}:{self.ip}:{self.port}'

    @property
    def url(self):
        if self.login and self.password:
            return f'{self.protocol}://{self.login}:{self.password}@{self.ip}:{self.port}/'
        else:
            return f'{self.protocol}://{self.ip}:{self.port}/'


    def check_proxy(self, *,no_proxy_ip):
        print(self)
        try:
            checkers_result = []
            for checker_class in (CheckProxyApi64, CheckProxyHttpBin):
                proxy_checker = checker_class(self.url, no_proxy_ip=no_proxy_ip)
                proxy_checker()
                if proxy_checker.is_work:
                    checkers_result.append(True)
                else:
                    checkers_result.append(False)
            if all(checkers_result):
                self.status = Proxy.WORK
                self.error_text = ''
            else:
                self.status = Proxy.NOT_WORK
                self.error_text = 'diff checkers result'
        except ConnectTimeout:
            self.error_text = 'Time out error'
            self.status = Proxy.NOT_WORK
        except CodeNot200:
            self.error_text = 'Not 200 status code'
            self.status = Proxy.NOT_WORK
        except Exception as error:
            self.error_text = str(error)[:255]
            self.status = Proxy.NOT_WORK
        finally:
            self.save()

    @staticmethod
    def check_proxies(qs):
        no_proxy_ip = CheckProxyApi64.get_ip()
        print(no_proxy_ip, 'no_proxy_ip')
        for proxy_model in qs:
            proxy_model.check_proxy(no_proxy_ip=no_proxy_ip)


# class ProxyPassword(Proxy):
#     login = models.CharField(max_length=30)
#     password = models.CharField(max_length=30)
#
#
#     @property
#     def url(self):
#         return f'http://{self.login}:{self.password}@{self.data}/'


