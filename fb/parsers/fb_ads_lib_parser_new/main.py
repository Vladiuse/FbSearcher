from selenium import webdriver
from requests.models import PreparedRequest
from time import sleep
from selenium.webdriver.common.by import By
from cards import CardSearch
import time
from selenium.common.exceptions import NoSuchElementException

def log_links(links):
    with open('/home/vlad/links.txt', 'a') as file:
        for link in links:
            file.write(link + '\n')

class FbLibPage:
    URL_PARAMS = {'active_status': 'active',
                  # 'ad_type': 'political_and_issue_ads',
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

    CARDS_LOAD_COUNT = 30


    WAIT_AFTER_LOADING = 5
    MAX_WAIT_TIME_CARDS_LOAD = 20
    TIME_FOR_CARDS_LOADING = 3
    MAX_PAGE_ITERATION = 150
    BLOCK_CLASS_NAME = 'xxx'

    def __init__(self, *, q, start_date, country):
        self.q = q
        self.start_date = start_date
        self.country = country

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

    def remove_all_cards(self):
        DRIVER.execute_script("""
var cards = document.querySelectorAll('div.xrvj5dj.xdq2opy.xexx8yu.xbxaen2.x18d9i69.xbbxn1n.xdoe023.xbumo9q.x143o31f.x7sq92a.x1crum5w > div.xh8yej3')
for (let i=0; i < cards.length; i++){
    var card = cards[i]
    card.remove()
};
""")
    def click_load_new_js(self):
        DRIVER.execute_script("""
var load_new_button = document.querySelector('a._8n_3')
load_new_button.click()
                """)

    def click_load_new_cards(self):

        for _ in range(10):
            print('wait load new button')
            sleep(1)
            try:
                button = DRIVER.find_element(By.CSS_SELECTOR, 'a._8n_3')
                print('Button found')
                sleep(1)
                if button:
                    self.click_load_new_js()
                    # button.click()
                    return
            except NoSuchElementException as error:
                pass
        raise ZeroDivisionError('no click button')

    def hide_cards_media(self):
        DRIVER.execute_script("""
const styleNoMedia = document.createElement("style")
styleNoMedia.textContent = "div.xrvj5dj.xdq2opy.xexx8yu.xbxaen2.x18d9i69.xbbxn1n.xdoe023.xbumo9q.x143o31f.x7sq92a.x1crum5w > div.xh8yej3  ._7jyg._7jyh{display:none;}"
document.head.appendChild(styleNoMedia)
        """)

    def cards_count(self):
        cards = DRIVER.find_elements(By.CSS_SELECTOR, 'div.xrvj5dj.xdq2opy.xexx8yu.xbxaen2.x18d9i69.xbbxn1n.xdoe023.xbumo9q.x143o31f.x7sq92a.x1crum5w > div.xh8yej3')
        return len(cards)

    def get_links(self):
        html = str(DRIVER.page_source)
        cards_searcher = CardSearch(html)
        return cards_searcher.links

    def run(self):
        # self.hide_cards_media()
        input('Start main?')
        for _ in range(20):
            self._wait_cards_load()
            links = self.get_links()
            log_links(links)
            print('Links count:', len(links))
            sleep(3)
            self.remove_all_cards()
            self.click_load_new_cards()

    def _wait_cards_load(self):
        print('Start wait cards')
        start = time.time()
        while True:
            cards_count = self.cards_count()
            print('Cards on page', cards_count)
            if cards_count:
                break
            else:
                if time.time() - start > self.MAX_WAIT_TIME_CARDS_LOAD:
                    raise ZeroDivisionError
                else:
                    sleep(1)
                    continue




WINDOW_SIZE = (1200, 800)
DRIVER = webdriver.Chrome()
DRIVER.set_window_size(*WINDOW_SIZE)


fb_lib_page = FbLibPage(q='main', country='US', start_date='2023-10-16')
DRIVER.get(fb_lib_page.url)
fb_lib_page.run()