from proxies.models import ProxyMobile, ProxyChangeIpUrlNotWork,ProxyChangeIpTimeOutError
from django.test import TestCase
from unittest.mock import patch
from unittest import mock
from requests.exceptions import RequestException

def create_mobile_proxy():
    proxy = ProxyMobile.objects.create(
        ip='1',
        port='2020',
        login='1',
        password='1',
        change_ip_url='https://google.com/'
    )
    return proxy

class TestClickChangeProxyIpUrlTest(TestCase):

    def setUp(self):
        self.proxy = create_mobile_proxy()

    def test_click_on_change_ip_url_all_good(self):
        with patch('requests.get',) as mock:
            mock.return_value.status_code = 200
            self.proxy._click_change_ip_url()

    def test_click_on_change_ip_url_not_200(self):
        with patch('requests.get',) as mock:
            mock.return_value.status_code = 1
            with self.assertRaises(ProxyChangeIpUrlNotWork):
                self.proxy._click_change_ip_url()

    def test_click_on_change_ip_url_some_error(self):
        with patch('requests.get', side_effect=RequestException) as mock:
            with self.assertRaises(ProxyChangeIpUrlNotWork):
                self.proxy._click_change_ip_url()


class ChangeProxyIpTest(TestCase):

    def setUp(self):
        self.proxy = create_mobile_proxy()

    def test_all_ip_not_changed(self):
        with patch('time.sleep',side_effect=None):
            with patch('requests.get',) as mock:
                mock.return_value.status_code = 200
                with patch('proxies.check_proxies.get_current_ip', return_value='123'):
                    with patch('proxies.check_proxies.get_proxy_ip', return_value='123'):
                        with self.assertRaises(ProxyChangeIpTimeOutError):
                            self.proxy.change_ip()

    def test_ip_not_changed(self):
        with patch('time.sleep',side_effect=None):
            with patch('requests.get',) as mock:
                mock.return_value.status_code = 200
                with patch('proxies.check_proxies.get_current_ip', return_value='123'):
                    with patch('proxies.check_proxies.get_proxy_ip', return_value='xxx'):
                        with self.assertRaises(ProxyChangeIpTimeOutError):
                            self.proxy.change_ip()


    def test_ip_not_changed_2(self):
        with patch('time.sleep',side_effect=None):
            with patch('requests.get',) as mock:
                mock.return_value.status_code = 200
                with patch('proxies.check_proxies.get_current_ip', return_value='123'):
                    with patch('proxies.check_proxies.get_proxy_ip', side_effect=['yyy','xxx']):
                        self.proxy.change_ip()


    # def test_spleep(self):
    #     with patch('time.sleep',side_effect=RequestException ) as mock:
    #         self.proxy.test_sleep()




