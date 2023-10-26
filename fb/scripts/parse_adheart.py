from selenium import webdriver
import os
from time import sleep
import random as r
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from time import time
import pickle
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By


COOKIE_PATH = 'cookies_adheart.pkl'
LOG_FILE = '/home/vlad/links_heart.txt'


def log_links(links):
    with open(LOG_FILE, 'a') as file:
        for link in links:
            file.write(link + '\n')

#url = f'https://adheart.me/teasers/?platforms[]=facebook&geos[]={GEO}&last_active_at={DAYS}&categories=Array&use_blacklist=false&page={i}'

class AdHeartDriverParser:
    MAX_WAIT_TIME_CARDS_LOAD = 45

    def __init__(self,start_page=1):
        self.start_page = start_page
        self.days = 1
        self.pages_count = 0

    def cards_count(self):
        cards = DRIVER.find_elements(By.CSS_SELECTOR, '.card.card-blog')
        return len(cards)

    def get_links(self):
        links = []
        html = DRIVER.page_source
        soup = BeautifulSoup(html, 'lxml')
        cards = soup.select('.media')
        for card in cards:
            link = card.select_one('h4 a')
            if link:
                try:
                    links.append(link['href'])
                except KeyError:
                    print('KeyError')
        print('Cards found', len(cards), 'Links found', len(links))
        return links

    def remove_all_cards(self):
        DRIVER.execute_script("""
var cards = document.querySelectorAll('.card.card-blog')
for (let i = 0; i < cards.length; i++){
    var card = cards[i]
    card.remove()
}
        """)

    def _hide_cards_media(self):
        DRIVER.execute_script(
            """
const styleNoMedia = document.createElement("style")
styleNoMedia.textContent = ".card.card-blog .carousel.slide{display: none;}"
document.head.appendChild(styleNoMedia)
            """
        )

    def _hide_hr(self):
        DRIVER.execute_script(
            """
const styleHr = document.createElement("style")
styleHr.textContent = "hr{display: none;}"
document.head.appendChild(styleHr)
            """
        )

    def _wait_cards_load(self):
        sleep(r.uniform(8,10))
        start = time()
        while True:
            links = self.cards_count()
            if links:
                break
            else:
                sleep(0.5)
                if time() - start > self.MAX_WAIT_TIME_CARDS_LOAD:
                    raise ZeroDivisionError('Max wait cards load')
                else:
                    pass

    def run(self):
        DRIVER.get(f'https://adheart.me/teasers/?last_active_at={self.days}&platforms[]=facebook&categories=Array&use_blacklist=false&page={self.start_page}')
        input('Start? ')
        self._hide_cards_media()
        self._hide_hr()
        while True:
            self._wait_cards_load()
            links = self.get_links()
            log_links(links)
            self.remove_all_cards()
            self.pages_count += 1
            print('Page', self.pages_count)

DRIVER = webdriver.Chrome()
DRIVER.get('https://adheart.me/ru/dashboard')
if os.path.exists(COOKIE_PATH):
    cookies = pickle.load(open(COOKIE_PATH, "rb"))
    for cookie in cookies:
        DRIVER.add_cookie(cookie)
DRIVER.get('https://adheart.me/ru/dashboard')
pickle.dump(DRIVER.get_cookies(), open(COOKIE_PATH, "wb"))

adheart_parser = AdHeartDriverParser(start_page=450)
adheart_parser.run()