from bs4 import BeautifulSoup



class FbMainPage:

    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, 'lxml')

    def _is_register_page(self):
        fb_login_image = self.soup.find('img', {'src': 'https://static.xx.fbcdn.net/rsrc.php/yu/r/dyZbZB6M64R.svg'})
        fb_login_form = self.soup.find('form', {'class': '_9vtf'})
        return bool(fb_login_image and fb_login_form)

    def _is_auth_page(self):
        if self.soup.find('div', {'id': 'splash-screen'}):
            return True
        return False
    @property
    def is_login(self):
        is_register_page = self._is_register_page()
        is_auth_page = self._is_auth_page()
        if  is_register_page ==  is_auth_page:
            raise TypeError('Значения не должны быть равны')
        return not is_register_page and is_auth_page

if __name__ == '__name__':

    FB_MAIN_LOGIN_PAGE_PASE = '/home/vlad/PycharmProjects/FbSearcher/fb/parsers/fb_pages_html/fb_main_login.html'
    FB_MAIN_NO_LOGIN_PAGE_PASE = '/home/vlad/PycharmProjects/FbSearcher/fb/parsers/fb_pages_html/fb_main_no_login.html'
    with open(FB_MAIN_NO_LOGIN_PAGE_PASE) as file:
        html_no_login = file.read()

    with open(FB_MAIN_LOGIN_PAGE_PASE) as file:
        html_login = file.read()
    page = FbMainPage(html_no_login)
    print(page.is_login)
