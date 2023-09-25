from bs4 import BeautifulSoup
import re

class NotFoundGroupNameError(Exception):
    """Не найдено название группы при наличии тега"""


class FbGroupPage:
    SLEEP_AFTER_LOAD = 1

    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, 'lxml')
        self.group_name = None
        self.group_email = None

    def __call__(self):
        self.get_group_name()
        self.get_group_email()

    @property
    def is_auth(self):
        return bool(self.group_name)


    @property
    def result(self):
        res = {}
        if self.group_email:
            res.update({ 'group_email': self.group_email})
        if self.group_name:
            res.update({'group_name': self.group_name})
        return res


    def get_group_name(self):
        h1_block = self.soup.find('h1', class_='x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz')
        if h1_block:
            if h1_block.find('span'):
                span = h1_block.find('span')
                span.extract()
            self.group_name = h1_block.get_text().strip()
            if not self.group_name:
                raise NotFoundGroupNameError

    def get_group_email(self):
        email_icon_element = self.soup.find('img',
                                       {'src': 'https://static.xx.fbcdn.net/rsrc.php/v3/yE/r/2PIcyqpptfD.png'})
        if email_icon_element:
            email_text_content = email_icon_element.parent.parent.get_text().strip()
            self.group_email = email_text_content


    def find_mail_regex(self):
        match = re.search('[\w\-.]{2,50}@[\w\-.]{1,20}', self.html)


if __name__ == '__main__':
    fb_group_no_login_html_path = '/home/vlad/PycharmProjects/FbSearcher/fb/parsers/fb_pages_html/group_page/group_no_login.html'
    fb_group_login_html_path = '/home/vlad/PycharmProjects/FbSearcher/fb/parsers/fb_pages_html/group_page/group_login_mail.html'
    fb_group_login_html_path_no_email = '/home/vlad/PycharmProjects/FbSearcher/fb/parsers/fb_pages_html/group_page/group_login_no_mail.html'
    with open(fb_group_no_login_html_path) as file:
        no_login_page = FbGroupPage(file.read())
        no_login_page()
    with open(fb_group_login_html_path) as file:
        login_page = FbGroupPage(file.read())
        login_page()
    with open(fb_group_login_html_path_no_email) as file:
        login_page_no_email = FbGroupPage(file.read())
        login_page_no_email()
    print('NO LOGIN', no_login_page.is_auth, no_login_page.result)
    print('LOGIN EMAIL', login_page.is_auth, login_page.result)
    print('LOGIN NO EMAIL', login_page_no_email.is_auth, login_page_no_email.result)



