import requests as req
from requests.exceptions import RequestException, ProxyError, Timeout
from json.decoder import JSONDecodeError


class CodeNot200(Exception):
    """not 200 status code check proxy"""


class CheckerNotWorkError(Exception):
    """Checker class not work"""

class ProxyIpNotChange(Exception):
    """proxy ip equal ip without proxy"""


class CheckProxy:
    CHECK_TIMEOUT = 10
    GET_MY_IP = ''

    def __init__(self):
        self.__ip = None
        self.error = None
        self.status_code = None

    def _get_ip(self, proxy_url=None):
        """Получить ip"""
        if proxy_url:
            proxies = {'https': proxy_url}
        else:
            proxies = {}
        try:
            res = req.get(self.GET_MY_IP, timeout=CheckProxy.CHECK_TIMEOUT, proxies=proxies)
            if not res.status_code == 200:
                self.status_code = res.status_code
                raise CodeNot200
            self.__ip = self._get_ip_from_response(res)
        except (Timeout, ProxyError, RequestException) as error:
            self.error = error
            self.error_text = str(error)
        except CodeNot200 as error:
            self.error = error
            self.error_text = 'Not 200 status code'
        except JSONDecodeError as error:
            self.error = error
            self.error_text = 'Cant parse ip from response'

    def get_ip(self) -> str:
        """Получить ip без прокси"""
        self._get_ip()
        return self.__ip

    def get_proxy_ip(self, proxy_url) -> str:
        """Получить ip под прокси"""
        self._get_ip(proxy_url=proxy_url)
        return self.__ip

    @staticmethod
    def _get_ip_from_response(res) -> str:
        """Получить  ip из ответа сервиса"""
        raise NotImplementedError


class CheckProxyApi64(CheckProxy):
    GET_MY_IP = 'https://api64.ipify.org?format=json'

    @staticmethod
    def _get_ip_from_response(res) -> str:
        """Получить  ip из ответа сервиса"""
        ip = res.json()['ip']
        return ip


class CheckProxyHttpBin(CheckProxy):
    GET_MY_IP = 'https://httpbin.org/ip'

    @staticmethod
    def _get_ip_from_response(res) -> str:
        """Получить  ip из ответа сервиса"""
        ip = res.json()['origin']
        return ip


class CheckProxyMyIp(CheckProxy):
    GET_MY_IP = 'https://api.myip.com/'

    @staticmethod
    def _get_ip_from_response(res) -> str:
        """Получить  ip из ответа сервиса"""
        ip = res.json()['ip']
        return ip


checkers_classes_list = (CheckProxyApi64, CheckProxyHttpBin, CheckProxyMyIp)


def get_current_ip():
    """Получить ip без прокси"""
    for checker_class in checkers_classes_list:
        checker = checker_class()
        ip = checker.get_ip()
        if ip:
            return ip
    raise CheckerNotWorkError('All checkers not work!')


def get_proxy_ip(proxy_url):
    """Получить ip под прокси"""
    for checker_class in checkers_classes_list:
        checker = checker_class()
        proxy_ip = checker.get_proxy_ip(proxy_url)
        if proxy_ip:
            return proxy_ip
    raise CheckerNotWorkError('All checkers not work!')


def check_proxy(proxy_url):
    """Работает ли прокси - должны отличаться айпишники"""
    current_ip = get_current_ip()
    proxy_ip = get_proxy_ip(proxy_url)
    if current_ip == proxy_ip:
        raise ProxyIpNotChange
    return proxy_ip


def _check_checkers():
    ips = []
    errors = []
    for checker_class in checkers_classes_list:
        checker = checker_class()
        try:
            ip = checker.get_ip()
            ips.append(ip)
        except CheckerNotWorkError as error:
            errors.append([checker, error])
    if len(ips) == len(checkers_classes_list) and not errors:
        assert all(ips) is True
        assert len(set(ips)) == 1
        print(f'All checkers work! You api is {ips[0]}')
    else:
        if errors:
            for checker, error in errors:
                print(f'Checker {checker} not work, error - {error}')
        if len(set(ips)) != 1:
            print(f'Ips not equal {ips}')



if __name__ == '__main__':
    _check_checkers()

