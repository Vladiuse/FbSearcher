from bs4 import BeautifulSoup
import re


class FbGroupPage:
    SLEEP_AFTER_LOAD = 1

    def __init__(self, html, user_cookie=True):
        self.html = html
        self.use_cookie = user_cookie
        self.soup = BeautifulSoup(html, 'html.parser')
        self.group_name = None
        self.group_email = None

    def __call__(self):
        if self.use_cookie:
            self.get_group_name_from_h1_with_cookie()
            self.group_email_with_cookie()
            if not self.group_email:
                self.get_group_email_with_reg_ex()
        else:
            self.get_group_name_from_title()
            self.get_group_email_from_script()

    @property
    def is_login_form(self):
        if 'https://static.xx.fbcdn.net/rsrc.php/y8/r/dF5SId3UHWd.svg' in self.html:
            return True
        return False


    @property
    def result(self):
        res = {}
        if self.group_email:
            res.update({ 'group_email': self.group_email})
        if self.group_name:
            res.update({'group_name': self.group_name})
        return res


    def get_group_name_from_h1_with_cookie(self):
        h1_block = self.soup.find('h1', class_='x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz')
        if h1_block:
            self.group_name = h1_block.text

    def group_email_with_cookie(self):
        email_icon_element = self.soup.find('img',
                                       {'src': 'https://static.xx.fbcdn.net/rsrc.php/v3/yE/r/2PIcyqpptfD.png'})
        if email_icon_element:
            email_text_content = email_icon_element.parent.parent.get_text().strip()
            self.group_email = email_text_content

    def get_group_email_with_reg_ex(self):
        # [\w\\.]{1,100}\u0040[\w\\.\-_]{1,100}
        email_match = re.match(r'[\w\\.]{1,100}@[\w\\.\-_]{1,100}', self.html)
        if email_match:
            return email_match[0]

    def get_group_name_from_title(self):
        """Если нет кука"""
        title = self.soup.find('title')
        if title:
            group_name = self._get_group_name_from_title(title.text)
            self.group_name = group_name

    def _get_group_name_from_title(self, title):
        """Отделить имя групи в титле"""
        group_name = title
        if '|' in title:
            group_name, *others = title.split('|')
        return group_name.strip()

    def get_group_email_from_script(self):
        """При запросе без кука"""
        email_match = re.search( r'"text"\s{0,10}:\s{0,10}"[\w\\.]{1,100}\\u0040[\w\\.]{1,100}"|"text"\s{0,10}:\s{0,10}"[\w\\.]{1,100}@[\w\\.]{1,100}"', str(self.soup))
        if email_match:
            email_text = email_match[0]
            email = email_text.split(':')[-1].replace('"', '').replace('\\u0040', '@')
            self.group_email= email


if __name__ == '__main__':
    fb_group_no_login_html_path = '/home/vlad/PycharmProjects/FbSearcher/fb/parsers/fb_pages_html/group_page/group_no_login.html'
    fb_group_login_html_path = '/home/vlad/PycharmProjects/FbSearcher/fb/parsers/fb_pages_html/group_page/group_login.html'
    with open(fb_group_no_login_html_path) as file:
        no_login_page = FbGroupPage(file.read())

    with open(fb_group_login_html_path) as file:
        login_page = FbGroupPage(file.read())

    print('NO')



