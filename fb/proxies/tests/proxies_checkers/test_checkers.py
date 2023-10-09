import unittest
from unittest.mock import patch
from proxies.check_proxies import CheckProxy, CheckProxyApi64, CheckProxyHttpBin, CheckProxyMyIp
from proxies.check_proxies import get_current_ip, get_proxy_ip,check_proxy
from proxies.check_proxies import CodeNot200,CheckerNotWorkError
from time import sleep
from requests.exceptions import RequestException, ProxyError, Timeout
from json.decoder import JSONDecodeError


# return_value = '{"ip":"178.120.66.252"}'
def call_json_error(*args, **kwargs):
    raise JSONDecodeError('1', '1', 1)

class CheckerClassTest(unittest.TestCase):

    def test_get_ip_not_use_main_class(self):
        with patch('requests.get', ) as mock:
            with self.assertRaises(NotImplementedError):
                mock.return_value.status_code = 200
                mock.text = '{"ip":"178.120.66.252"}'
                checker = CheckProxy()
                checker._get_ip()

    def test_not_200_status_code(self):
        checker = CheckProxyApi64()
        with patch('requests.get') as mock:
            mock.return_value.status_code = 199
            checker.get_ip()
            self.assertIsNotNone(checker.error)
            self.assertTrue(isinstance(checker.error, CodeNot200))

    def test_timeout(self):
        checker = CheckProxyApi64()
        with patch('requests.get', side_effect=Timeout) as mock:
            checker.get_ip()
            self.assertIsNotNone(checker.error)
            self.assertTrue(isinstance(checker.error, Timeout))

    def test_proxy_error(self):
        checker = CheckProxyApi64()
        with patch('requests.get', side_effect=ProxyError) as mock:
            checker.get_ip()
            self.assertIsNotNone(checker.error)
            self.assertTrue(isinstance(checker.error, ProxyError))

    def test_request_error(self):
        checker = CheckProxyApi64()
        with patch('requests.get', side_effect=RequestException) as mock:
            checker.get_ip()
            self.assertIsNotNone(checker.error)
            self.assertTrue(isinstance(checker.error, RequestException))

    def test_json_error(self):
        checker = CheckProxyApi64()
        with patch('requests.get', ) as mock:
            mock.return_value.status_code = 200
            mock.return_value.json = call_json_error
            ip = checker.get_ip()
            self.assertIsNotNone(checker.error)
            self.assertTrue(isinstance(checker.error, JSONDecodeError))

    def test_incorrect_dict_from_service(self):
        checker = CheckProxyApi64()
        with patch('requests.get', ) as mock:
            mock.return_value.status_code = 200
            mock.return_value.json = lambda : {}
            with self.assertRaises(KeyError):
                ip = checker.get_ip()

    def test_all_good_CheckProxyApi64(self):
        with patch('requests.get', ) as mock:
            mock.return_value.status_code = 200
            mock.return_value.json = lambda :{"ip":"178.120.66.252"}
            checker = CheckProxyApi64()
            ip = checker.get_ip()
            self.assertIsNone(checker.error)
            self.assertEqual(ip,"178.120.66.252")

    def test_all_good_CheckProxyHttpBin(self):
        with patch('requests.get', ) as mock:
            mock.return_value.status_code = 200
            mock.return_value.json = lambda :{"origin":"178.120.66.252"}
            checker = CheckProxyHttpBin()
            ip = checker.get_ip()
            self.assertIsNone(checker.error)
            self.assertEqual(ip,"178.120.66.252")

    def test_all_good_CheckProxyMyIp(self):
        with patch('requests.get', ) as mock:
            mock.return_value.status_code = 200
            mock.return_value.json = lambda :{"ip":"178.120.66.252"}
            checker = CheckProxyMyIp()
            ip = checker.get_ip()
            self.assertIsNone(checker.error)
            self.assertEqual(ip,"178.120.66.252")


class GetIpFuncTest(unittest.TestCase):

    def test_all_good(self):
        with patch.object(CheckProxyApi64, 'get_ip', return_value='xxx') as mock:
            ip = get_current_ip()
            self.assertEqual(ip, 'xxx')

    def test_all_good_first_service_not_work(self):
        with patch.object(CheckProxyApi64, 'get_ip', return_value=None) as mock:
            with patch.object(CheckProxyHttpBin, 'get_ip', return_value='xxx') as mock:
                ip = get_current_ip()
                self.assertEqual(ip, 'xxx')

    def test_all_good_first_two_service_not_work(self):
        with patch.object(CheckProxyApi64, 'get_ip', return_value=None) as mock:
            with patch.object(CheckProxyHttpBin, 'get_ip', return_value=None) as mock:
                with patch.object(CheckProxyMyIp, 'get_ip', return_value='xxx') as mock:
                    ip = get_current_ip()
                    self.assertEqual(ip, 'xxx')

    def test_all_service_not_work(self):
        with patch.object(CheckProxyApi64, 'get_ip', return_value=None) as mock:
            with patch.object(CheckProxyHttpBin, 'get_ip', return_value=None) as mock:
                with patch.object(CheckProxyMyIp, 'get_ip', return_value=None) as mock:
                    with self.assertRaises(CheckerNotWorkError):
                        ip = get_current_ip()


class GetProxyIpTest(unittest.TestCase):
    def test_all_good(self):
        with patch.object(CheckProxyApi64, 'get_proxy_ip', return_value='xxx') as mock:
            ip = get_proxy_ip(1)
            self.assertEqual(ip, 'xxx')

    def test_all_good_first_service_not_work(self):
        with patch.object(CheckProxyApi64, 'get_proxy_ip', return_value=None) as mock:
            with patch.object(CheckProxyHttpBin, 'get_proxy_ip', return_value='xxx') as mock:
                ip = get_proxy_ip(1)
                self.assertEqual(ip, 'xxx')

    def test_all_good_first_two_service_not_work(self):
        with patch.object(CheckProxyApi64, 'get_proxy_ip', return_value=None) as mock:
            with patch.object(CheckProxyHttpBin, 'get_proxy_ip', return_value=None) as mock:
                with patch.object(CheckProxyMyIp, 'get_proxy_ip', return_value='xxx') as mock:
                    ip = get_proxy_ip(1)
                    self.assertEqual(ip, 'xxx')

    def test_all_service_not_work(self):
        with patch.object(CheckProxyApi64, 'get_proxy_ip', return_value=None) as mock:
            with patch.object(CheckProxyHttpBin, 'get_proxy_ip', return_value=None) as mock:
                with patch.object(CheckProxyMyIp, 'get_proxy_ip', return_value=None) as mock:
                    with self.assertRaises(CheckerNotWorkError):
                        ip = get_proxy_ip(1)





