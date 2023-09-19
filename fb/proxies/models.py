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
    data = models.CharField(max_length=255, unique=True)
    status = models.BooleanField(max_length=50,  default=NOT_CHECKED, null=True)
    error_text = models.CharField(max_length=255, blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'<Proxy:{self.pk}> {self.data}'

    @property
    def url(self):
        return f'socks5://{self.data}/'

    def check_proxy(self, *,no_proxy_ip):
        print(self)
        try:
            checkers_result = []
            for checker_class in (CheckProxyApi64, CheckProxyHttpBin):
                proxy_checker = checker_class(self.data, no_proxy_ip=no_proxy_ip)
                proxy_checker()
                if proxy_checker.is_work:
                    checkers_result.append(True)
                else:
                    checkers_result.append(False)
            if all(checkers_result):
                self.status = Proxy.WORK
            else:
                self.status = Proxy.NOT_WORK
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



