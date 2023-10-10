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
        self.regex_email = None
        self.regex_name = None
        self.title = self._get_title()

    def __call__(self):
        self.get_group_name()
        self.find_email()

    def _get_title(self):
        title = self.soup.find('title')
        if title:
            return title.text.strip()

    def find_email(self):
        self.group_email = self.get_group_email_from_html_block()
        if not self.group_email:
            self.group_email = self.get_email_by_regex()

    @property
    def is_login_form(self):
        """Являеться ли страница страницей входа (сформой)"""
        return

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
        if self.title:
            res.update({'title': self.title})
        return res


    def get_group_name(self):
        """Достать имя группы из блока"""
        h1_block = self.soup.find('h1', class_='x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz')
        if h1_block:
            if h1_block.find('span'):
                span = h1_block.find('span')
                span.extract()
            self.group_name = h1_block.get_text().strip()
            if not self.group_name:
                raise NotFoundGroupNameError

    def get_group_email_from_html_block(self):
        """Достать мыло из блока"""
        email_icon_element = self.soup.find('img',
                                       {'src': 'https://static.xx.fbcdn.net/rsrc.php/v3/yE/r/2PIcyqpptfD.png'})
        if email_icon_element:
            email_text_content = email_icon_element.parent.parent.get_text().strip()
            return email_text_content

    def get_email_by_regex(self):
        """Найти мыло в коде (елси незалогинен)
        Пример: "text":"someemail@gmail.com"
        """
        res = re.search(r'"text":"[\w\d_-]{2,50}(\\u0040|@)[\w\d_-]{2,50}\.[\w]{2,6}"',
                         self.html)
        if res:
            email_text_in_code = res.group(0)
            email_text_in_code = email_text_in_code.replace('"text":"','')
            email_text_in_code = email_text_in_code.replace('"','')
            email_text_in_code = email_text_in_code.replace('\\u0040','@')
            return email_text_in_code


class FbGroupPageNoAuth:
    """Группа Фб ьез аутентификации"""

    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, 'lxml')
        self.email = None
        self.name = None
        self.followers = None
        self._title = None

    def __call__(self):
        self.name = self.get_name()
        self.email = self.get_email()
        self.followers = self.get_followers()
        setattr(self,'_is_call', True)

    @property
    def result(self):
        if not hasattr(self, '_is_call'):
            raise AttributeError('Call FbGroup before result')
        res = {}
        if self.email:
            res.update({ 'email': self.email})
        if self.name:
            res.update({'name': self.name})
        if self.followers:
            res.update({'followers': self.followers})
        if self._title:
            res.update({'title': self._title})
        return res

    def get_email(self):
        return self._get_email_by_regex()

    def get_name(self):
        return self._get_name_from_title()

    def get_followers(self):
        return self._get_followers_from_code()

    def _get_name_from_title(self):
        title = self.soup.find('title')
        if title:
            self._title = title.text
            if '|' in title.text:
                name, *other = title.text.split('|')
                return name.strip()
            else:
                return title.text.strip()

    def _get_email_by_regex(self):
        """Найти мыло в коде (елси незалогинен)
        Пример: "text":"someemail@gmail.com"
        """
        res = re.search(r'"text":"[\w\d_-]{2,50}(\\u0040|@)[\w\d_-]{2,50}\.[\w]{2,6}"',
                         self.html)
        if res:
            email_text_in_code = res.group(0)
            email_text_in_code = email_text_in_code.replace('"text":"','')
            email_text_in_code = email_text_in_code.replace('"','')
            email_text_in_code = email_text_in_code.replace('\\u0040','@')
            return email_text_in_code

    def _get_name_from_code(self):
        var = 'profile_header_renderer'
        pos = self.html.find(var)
        if pos != -1:
            string = self.html[pos:pos+1000]
            match = re.search('"name":"[^"]{3,255}"', string)
            if match:
                group_name = match.group(0)
                group_name = group_name.replace('"name":"', '')
                group_name = group_name.replace('"', '')
                return group_name

    def _get_followers_from_code(self):
        res = re.search(r'"text":"[\d.]{1,6}[KkMm]? followers"', self.html)
        if res:
            followers = res.group(0)
            for string in ('"text":"', '"', 'followers'):
                followers = followers.replace(string, '')
            return followers.strip()



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



