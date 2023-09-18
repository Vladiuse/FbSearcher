from django.db import models
from .check_proxies import CheckProxyApi64, CheckProxyHttpBin, CodeNot200
from requests.exceptions import ConnectTimeout

class Proxy(models.Model):
    WORK = 'work'
    NOT_WORK = 'not_work'
    NOT_CHECKED = 'no_checked'
    STATUSES = (
        (WORK, 'Работает'),
        (NOT_WORK, 'Не работает'),
        (NOT_CHECKED, 'Не проверен'),
    )
    data = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50, choices=STATUSES, default=NOT_CHECKED)
    error_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'<Proxy:{self.pk}> {self.data}'

    @property
    def url(self):
        return f'socks5://{self.data}/'

    def check_proxy(self):
        print(self)
        try:
            checkers_result = []
            for checker_class in (CheckProxyApi64, CheckProxyHttpBin):
                proxy_checker = checker_class(self.data)
                proxy_checker()
                if proxy_checker.is_work:
                    checkers_result.append(True)
                else:
                    checkers_result.append(False)
            if all(checkers_result):
                self.status = Proxy.WORK
            else:
                self.status = Proxy.NOT_WORK
            self.save()
        except ConnectTimeout:
            self.error_text = 'Time out error'
            self.save()
        except CodeNot200:
            self.error_text = 'Not 200 status code'
            self.save()
