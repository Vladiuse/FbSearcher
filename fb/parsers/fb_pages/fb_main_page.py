import os

from bs4 import BeautifulSoup
import re


class FbPageError(Exception):
    def __init__(self, msg=''):
        self.msg = msg

class FbMainPage:
    URL = 'https://facebook.com/'

    BAN_MESSAGES = [
        'We suspended your account',
        '180 days',
        '180 \\u',
    ]

    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, 'lxml')

    def _is_register_page(self):
        return '"ACCOUNT_ID":"0","USER_ID":"0"' in self.html

    def _is_auth_page(self):
        return bool(re.search('"ACCOUNT_ID":"\d{8,18}","USER_ID":"\d{8,18}",', self.html))

    @property
    def is_auth(self):
        """Являеться страница страницей пользователя(залогиненого)"""
        is_register_page = self._is_register_page()
        is_auth_page = self._is_auth_page()
        if is_register_page == is_auth_page:
            raise FbPageError('Лог/разлог не определен')
        return not is_register_page and is_auth_page

    @property
    def is_ban(self):
        return any(msg in self.html for msg in self.BAN_MESSAGES)


class FbMainPageOld:
    URL = 'https://facebook.com/'

    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, 'lxml')

    def _is_register_page(self):
        """Являеться ли страница страницей входа в фейсбук"""
        # fb_login_image = self.soup.find('img', {'src': 'https://static.xx.fbcdn.net/rsrc.php/yu/r/dyZbZB6M64R.svg'})
        fb_login_image = 'src="https://static.xx.fbcdn.net/rsrc.php' in self.html
        fb_login_form = self.soup.find('form', {'class': '_9vtf'})
        return bool(fb_login_image and fb_login_form)

    def _is_auth_page(self):
        """Найти блок указывающий на то что пользователь залогинен"""
        if self.soup.find('div', {'id': 'splash-screen'}):
            return True
        return False

    @property
    def is_auth(self):
        """Являеться страница страницей пользователя(залогиненого)"""
        is_register_page = self._is_register_page()
        is_auth_page = self._is_auth_page()
        if  is_register_page ==  is_auth_page:
            raise TypeError('Значения не должны быть равны')
        return not is_register_page and is_auth_page



if __name__ == '__main__':
    main_no_login_path = '/home/vlad/PycharmProjects/FbSearcher/fb/parsers/fb_pages_html/main_page/fb_main_no_login.html'
    main_login_path = '/home/vlad/PycharmProjects/FbSearcher/fb/parsers/fb_pages_html/main_page/fb_main_login.html'
    main_login_180_ban_path = '/home/vlad/PycharmProjects/FbSearcher/fb/parsers/fb_pages_html/main_page_180_ban/6_test 3.html'
    main_no_login = FbMainPage(open(main_no_login_path).read())
    main_login = FbMainPage(open(main_login_path).read())
    main_login_ban = FbMainPage(open(main_login_180_ban_path).read())
    print(main_no_login.is_auth, main_no_login.is_ban)
    print(main_login.is_auth, main_login.is_ban)
    print(main_login_ban.is_auth, main_login_ban.is_ban)

