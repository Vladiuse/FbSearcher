import requests as req
from requests.models import PreparedRequest
import string
import random as r
from selenium import webdriver
from time import sleep
from time import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from parse_page import CardSearch, Cards

class MaxWaitNewPageTimeError(Exception):
    """превышено время одидания новой страницы"""

class LibraryPage:
    URL_PARAMS = {'active_status': 'all',
                  'ad_type': 'all',
                  'country': 'BY',
                  'q': None,
                  'sort_data[direction]': 'desc',
                  'sort_data[mode]': 'relevancy_monthly_grouped',
                  'search_type': 'keyword_unordered',
                  'media_type': 'all'}

    WINDOW_SIZE = (1200,800)
    CARDS_LOAD_COUNT = 30
    SLEEP_AFTER_SET_FILTER = 2
    WAIT_AFTER_PAGE_DOWN = 10
    MAX_WAIT_TIME_NEW_PAGE = 30
    TIME_FOR_CARDS_LOADING = 5

    BLOCK_CLASS_NAME = 'xxx'

    def __init__(self,q):
        self._url = 'https://www.facebook.com/ads/library/'
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(*LibraryPage.WINDOW_SIZE)
        self.q = q
        self.page_height = 0
        # self.no_height_change_count = 0
        self.current_page = 0
        self.pages_count = None

    def __iter__(self):
        self.i = 1
        return self

    def _get_params(self):
        params = self.URL_PARAMS
        params['q'] = self.q
        return params

    def _prepare_url(self):
        prepare = PreparedRequest()
        prepare.prepare_url(self._url, self._get_params())
        return prepare.url

    @property
    def url(self):
        return self._prepare_url()

    def open(self):
        self.browser.get(self.url)
        self.set_filters()
        sleep(self.SLEEP_AFTER_SET_FILTER)
        self._get_pages_count()

    def get_html(self):
        return str(self.browser.page_source)

    def set_filters(self):
        input('Выставте нужные фильтны и нажмите Enter: ')

    def __next__(self):
        self.current_page += 1
        print(f'Страница {self.current_page} из ~{self.pages_count}')
        if self.current_page == 1:
            return self.get_html()
        self._mark_cards_as_loaded()
        self.page_height = self._get_page_height()
        self._press_down_key()
        sleep(self.TIME_FOR_CARDS_LOADING)
        start = time()
        while True:
            if self._is_height_change:
                break
            else:
                if time() - start > self.MAX_WAIT_TIME_NEW_PAGE:
                    with open('fb_site_example/index.html', 'w') as file:
                        file.write(self.get_html())
                    raise StopIteration
            sleep(1)
        return self.get_html()


    def _mark_cards_as_loaded(self):
        script = """
cards = document.querySelectorAll('.xh8yej3:not(.xxx)')
cards.forEach(element => {
element.classList.add('xxx')
});
        """
        self.browser.execute_script(script)


    def _press_down_key(self):
        self.browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)

    def _get_page_height(self):
        body = self.browser.find_element(By.CSS_SELECTOR, 'body')
        return body.size['height']

    @property
    def _is_height_change(self):
        return self.page_height < self._get_page_height()

    def _get_count_of_adds(self):
        block = self.browser.find_element(By.CSS_SELECTOR, 'div.xdbano7')
        block_w_text = block.find_element(By.CSS_SELECTOR, 'div.x8t9es0.x1uxerd5.xrohxju')
        cards_count = ''.join(filter(lambda x: x.isdigit(),block_w_text.text))
        return cards_count

    def _get_pages_count(self):
        adds_count = self._get_count_of_adds()
        try:
            count = int(adds_count)
            pages_count = round(count / self.CARDS_LOAD_COUNT) + 1
            self.pages_count = pages_count
        except ValueError:
            self.pages_count = 'Неопределено'

if __name__ == '__main__':
    cards = Cards()
    fb_page = LibraryPage(q='дом')
    fb_page.open()
    for page in fb_page:
        card_searcher = CardSearch(page)
        find_cards = card_searcher()
        cards.extend(find_cards)
    for i in cards:
        print(i.print())
        break
    print('Карточек найдено', len(cards))