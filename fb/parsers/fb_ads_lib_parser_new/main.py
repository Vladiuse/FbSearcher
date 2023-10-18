from selenium import webdriver
from seleniumwire import webdriver
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

    PAGES_FOR_KEY_WORK = 60


    MAX_WAIT_TIME_CARDS_LOAD = 30
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
        for _ in range(20):
            # print('wait load new button')
            sleep(1) # 1 is old value
            if self.cards_count():  # не кликать кнопку - если карточки стали загружаться автоматически
                return
            try:
                button = DRIVER.find_element(By.CSS_SELECTOR, 'a._8n_3')
                # print('Button found')
                sleep(0.5) # 1 is old value
                if button:
                    if self.cards_count():  # не кликать кнопку - если карточки стали загружаться автоматически
                        return
                    self.click_load_new_js()
                    # button.click()
                    return
            except NoSuchElementException as error:
                pass
        raise ZeroDivisionError('no click button found')

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
        self.hide_cards_media()
        # input('Start main?')
        sleep(5)
        for _ in range(self.PAGES_FOR_KEY_WORK):
            self._wait_cards_load()
            links = self.get_links()
            log_links(links)
            # print('Links count:', len(links))
            #sleep(1)
            self.remove_all_cards()
            # sleep(0.5)  # 3 is old value
            self.click_load_new_cards()

    def _wait_cards_load(self):
        # print('Start wait cards')
        start = time.time()
        while True:
            cards_count = self.cards_count()
            # print('Cards on page', cards_count)
            if cards_count:
                break
            else:
                if time.time() - start > self.MAX_WAIT_TIME_CARDS_LOAD:
                    raise ZeroDivisionError('MAX_WAIT_TIME_CARDS_LOAD')
                else:
                    sleep(0.2)
                    continue


PROXY = 'http://MeHeS7:Eb1Empua4ES6@nproxy.site:14569/'
options = {
	'proxy': {
        'https':PROXY,
	}
}

WINDOW_SIZE = (1200, 800)
DRIVER = webdriver.Chrome(
    #seleniumwire_options=options
)
DRIVER.set_window_size(*WINDOW_SIZE)
keys = [
    # 'when', 'price', 'mobile', 'when', 'game',
    # 'come', 'fix', 'internet', 'fire', 'live','over',
    #'night', 'like', 'woman'
    #'most',
    'see', 'only', 'way', 'many', 'his', 'give',
     'call', 'send', 'meet','time', 'day', 'summer',
    'and', 'free', 'home', 'pass', 'than', 'size', 'baby', 'star', 'wife', 'game',
]
# DRIVER.get('https://google.com/')
# input('Start?')
for key in keys:
    try:
        fb_lib_page = FbLibPage(q=key, country='US', start_date='2023-10-16')
        DRIVER.get(fb_lib_page.url)
        fb_lib_page.run()
    except Exception as error:
        print(error, key)
