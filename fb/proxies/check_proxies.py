import requests as req


class CodeNot200(Exception):
    pass


class CheckProxy:
    CHECK_TIMEOUT = 10
    GET_MY_IP = ''

    def __init__(self, proxy, no_proxy_ip=None):
        self.proxy = proxy
        self.no_proxy_ip = no_proxy_ip
        self.proxy_ip = None

    def __call__(self):
        if not self.no_proxy_ip:
            self.no_proxy_ip = self.get_ip()
        self.get_proxy_ip()

    @property
    def is_work(self) -> bool:
        return self.no_proxy_ip != self.proxy_ip

    @classmethod
    def get_ip(cls):
        res = req.get(cls.GET_MY_IP, timeout=CheckProxy.CHECK_TIMEOUT)
        if res.status_code == 200:
            return cls.get_ip_from_response(res)
        else:
            raise CodeNot200

    def get_proxy_ip(self):
        proxies = {
            'https': self.proxy,
            # 'http': self.proxy,
        }
        res = req.get(self.GET_MY_IP, proxies=proxies, timeout=CheckProxy.CHECK_TIMEOUT)
        if res.status_code == 200:
            self.proxy_ip = self.get_ip_from_response(res)
        else:
            raise CodeNot200

    @staticmethod
    def get_ip_from_response(res):
        raise NotImplementedError


class CheckProxyApi64(CheckProxy):
    GET_MY_IP = 'https://api64.ipify.org?format=json'

    @staticmethod
    def get_ip_from_response(res) -> str:
        ip = res.json()['ip']
        print(' 1 CheckProxyApi64', ip)
        return ip


class CheckProxyHttpBin(CheckProxy):
    GET_MY_IP = 'https://httpbin.org/ip'

    @staticmethod
    def get_ip_from_response(res) -> str:
        ip = res.json()['origin']
        print('1 CheckProxyHttpBin', ip)
        return ip
