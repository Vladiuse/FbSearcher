from selenium import webdriver
import os
from time import sleep
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()

# dir_path = '/home/vlad/PycharmProjects/FbSearcher/adheart'
# while True:
#     res = input('Enter file name or exit: ')
#     if res == 'exit':
#         driver.quit()
#     file_path = os.path.join(dir_path, res)
#     html = driver.execute_script("return document.body.innerHTML")
#     with open(file_path, 'w') as file:
#         file.write(html)
LOG_DIR = '/home/vlad/PycharmProjects/FbSearcher/adheart'
LOG_FILE = '/home/vlad/all.txt'
def get_links(html):
    links = []
    soup = BeautifulSoup(html, 'lxml')
    cards = soup.select('.media')
    for card in cards:
        link = card.select_one('h4 a')
        if link:
            try:
                links.append(link['href'])
            except KeyError:
                print('KeyError')
    print('Cards found', len(cards),'Links found', len(links))
    return links

def log_html(page_num, html):
    file_name=  f'{page_num}.html'
    file_path = os.path.join(LOG_DIR, file_name)
    with open(file_path, 'w') as file:
        file.write(html)

input('LOGIN: ')
# driver.set_page_load_timeout(2)
# for i in range(1,400):
#     print(i)
#     url = f'https://adheart.me/teasers/?platforms[]=facebook&geos[]=US&last_active_at=1&categories=Array&use_blacklist=false&page={i}'
#     try:
#         driver.get(url)
#     except TimeoutException:
#         print('TimeOut')
#     html = driver.execute_script("return document.body.innerHTML")
#     log_html(i,html)
#     links = get_links(html)
#     with open(LOG_FILE, 'a') as file:
#         for link in links:
#             file.write(link + '\n')

