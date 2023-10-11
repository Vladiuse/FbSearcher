from time import sleep
import random as r
from proxies.models import ProxyChangeIpUrlNotWork, ProxyChangeIpTimeOutError
from faker import Faker


f = Faker()

class ResponseFake:

    def __init__(self, status_code, text=None):
        self.status_code = status_code
        self.text = text


class RequestFake:

    # def get(self, url):
    #     if r.randint(0, 8) == 8:
    #         raise AttributeError
    #     choices = [
    #         Response(200, {'name': 'XXX', 'email': 'some@gmail.com'}),
    #         Response(200, {'name': 'XXX', }),
    #         Response(200, {}),
    #         Response(300),
    #     ]
    #     sleep(r.uniform(0.5, 1.5))
    #     return r.choice(choices)

    def get(self, url):
        choices = [
            {'status': True, 'result': {'name': 'name', 'email': 'some@com'}},
            {'status': True, 'result': {'name': 'name', }},
            {'status': True, 'result': {}},
            {'status': False, },
            {'status': False, 'error': 'status code not 200'},
        ]
        sleep(r.uniform(0.5, 1.5))
        return r.choice(choices)

class ProxyFake:

    def __init__(self):
        self.url = 'xxx'
        self.pk = r.randint(1,100)
        self.ip = f.ipv4()

    @property
    def current_ip(self):
        sleep(r.randint(1,3))
        return self.ip

    def change_ip(self):
        sleep(r.randint(3,6))
        choices = [
            self._set_new_ip,
            self._raise_change_ip_error,
        ]
        var = r.choice(choices)
        var()

    def _raise_change_ip_error(self):
        choices = [
            ProxyChangeIpUrlNotWork,
            ProxyChangeIpTimeOutError,
        ]
        raise r.choice(choices)

    def _set_new_ip(self):
        self.ip = self._get_random_ip()

    def _get_random_ip(self):
        return f.ipv4()