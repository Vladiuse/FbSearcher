import requests as req
from requests.models import PreparedRequest
import string
import random as r
from selenium import webdriver
from time import sleep
from time import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from .cards_class import CardSearch, Cards


class MaxWaitNewPageTimeError(Exception):
    """превышено время одидания новой страницы"""


class FbLibPage:
    URL_PARAMS = {'active_status': 'active',
                  'ad_type': 'all',
                  'country': None,
                  'q': None,
                  'sort_data[direction]': 'desc',
                  'sort_data[mode]': 'relevancy_monthly_grouped',
                  'search_type': 'keyword_unordered',
                  'media_type': 'all',
                  'start_date[min]': None,
                  'start_date[max]': '',
                  'publisher_platforms[0]': 'facebook',
                  }
    FB_LIB_URL = 'https://www.facebook.com/ads/library/'
    WINDOW_SIZE = (1200, 800)
    CARDS_LOAD_COUNT = 30
    WAIT_AFTER_LOADING = 5
    MAX_WAIT_TIME_NEW_PAGE = 20
    TIME_FOR_CARDS_LOADING = 3
    MAX_PAGE_ITERATION = 30
    BLOCK_CLASS_NAME = 'xxx'

    def __init__(self, *, q, start_date, country):
        self.q = q
        self.start_date = start_date
        self.country = country
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(*FbLibPage.WINDOW_SIZE)
        self.page_height = 0
        # self.no_height_change_count = 0
        self.current_page = 0
        self.pages_count = None

    def __iter__(self):
        self.i = 1
        return self

    def close(self):
        self.browser.close()

    def _get_params(self):
        params = self.URL_PARAMS
        params['q'] = self.q
        params['country'] = self.country
        params['start_date[min]'] = self.start_date
        return params

    def _prepare_url(self):
        prepare = PreparedRequest()
        prepare.prepare_url(self.FB_LIB_URL, self._get_params())
        return prepare.url

    @property
    def url(self):
        return self._prepare_url()

    def open(self):
        self.browser.get(self.url)
        sleep(self.WAIT_AFTER_LOADING)
        self._get_pages_count()

    def get_html(self):
        return str(self.browser.page_source)

    def set_filters(self):
        input('Выставте нужные фильтны и нажмите Enter: ')

    def __next__(self):
        self.current_page += 1
        if self.current_page >= self.MAX_PAGE_ITERATION:
            raise StopIteration
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
                    raise StopIteration
            sleep(1)
        return self.get_html()

    def destroy_old_cards(self):
        pass
    # TODO

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
        cards_count = ''.join(filter(lambda x: x.isdigit(), block_w_text.text))
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
    KEY_WORDS_RU = [
        # 'косметика', 'еда', 'животные', 'дом',
                    'стройка', 'игрушки', 'развлечения', 'отдых', 'вечеринки',
                 'ресторан', 'спорт', 'юрист', 'репетитор', 'курорт', 'развлечения', 'мебель', 'учеба', 'жизнь', 'электротехника']
    cards = Cards()
    for key_word in KEY_WORDS_RU:
        try:
            fb_page = FbLibPage(q=key_word, start_date='2023-09-10', country='BY')
            fb_page.open()
            for page in fb_page:
                card_searcher = CardSearch(page)
                find_cards = card_searcher()
                cards.extend(find_cards)
                cards.send_to_db()
            fb_page.close()
        except Exception as error:
            print(key_word, 'ERROR', error)
