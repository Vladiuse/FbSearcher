import requests as req

class CodeNot200(Exception):
    pass

class CheckProxy:
    GET_MY_IP = ''

    def __init__(self, proxy):
        self.proxy = proxy
        self.no_proxy_ip = None
        self.proxy_ip = None

    def __call__(self):
        self.get_ip()
        self.get_proxy_ip()

    @property
    def is_work(self):
        return self.no_proxy_ip != self.proxy_ip

    def get_ip(self):
        res = req.get(self.GET_MY_IP, timeout=10)
        if res.status_code == 200:
            self.no_proxy_ip = self.get_ip_from_response(res)
        else:
            raise CodeNot200

    def get_proxy_ip(self):
        proxies = {
        'https': self.proxy
        }
        res = req.get(self.GET_MY_IP, proxies=proxies, timeout=10)
        if res.status_code == 200:
            self.proxy_ip = self.get_ip_from_response(res)
        else:
            raise CodeNot200


    def get_ip_from_response(self, res):
        raise NotImplementedError


class CheckProxyApi64(CheckProxy):
    GET_MY_IP = 'https://api64.ipify.org?format=json'

    def get_ip_from_response(self, res):
        return res.json()['ip']


class CheckProxyHttpBin(CheckProxy):
    GET_MY_IP = 'https://httpbin.org/ip'

    def get_ip_from_response(self, res):
        return res.json()['origin']

