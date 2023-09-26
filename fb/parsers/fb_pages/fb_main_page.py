import os

from bs4 import BeautifulSoup
import re


class FbPageError(Exception):
    def __init__(self, msg=''):
        self.msg = msg

class FbMainPage:
    URL = 'https://facebook.com/'

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
    dir_path = '/home/vlad/PycharmProjects/FbSearcher/fb/media/test_account_cookie_auth'
    for file in os.listdir(dir_path):
        path = os.path.join(dir_path, file)
        with open(path) as file:
            html = file.read()
            page = FbMainPage(html)
            print(file, page.is_auth)

