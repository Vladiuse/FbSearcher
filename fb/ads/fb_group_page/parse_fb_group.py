from bs4 import BeautifulSoup
import re


class FbGroupPage:
    SLEEP_AFTER_LOAD = 1

    def __init__(self, html):
        self.soup =  BeautifulSoup(html, 'lxml')
        self.group_name = None
        self.group_email = None

    def __call__(self):
        self. group_name = self.get_group_name()
        self.group_email = self.get_group_email()

    @property
    def result(self):
        res = {}
        if self.group_email:
            res.update({ 'group_email': self.group_email})
        if self.group_name:
            res.update({'group_name': self.group_name})
        return res

    def _get_group_name_from_title(self, title):
        group_name = title
        if '|' in title:
            group_name, *others = title.split('|')
        return group_name.strip()


    def get_group_name(self):
        title = self.soup.find('title')
        if title:
            group_name = self._get_group_name_from_title(title.text)
            return group_name
        return ''

    def get_group_email(self):
        email_match = re.search( r'"text"\s{0,10}:\s{0,10}"[\w\\.]{1,100}\\u0040[\w\\.]{1,100}"|"text"\s{0,10}:\s{0,10}"[\w\\.]{1,100}@[\w\\.]{1,100}"', str(self.soup))
        if email_match:
            email_text = email_match[0]
            email = email_text.split(':')[-1].replace('"', '').replace('\\\\u0040', '@')
            return email
        return ''



