import requests as req
from bs4 import BeautifulSoup

class Card:

    def __init__(self, card_soup):
        self.soup = card_soup

    @property
    def is_active(self):
        return 'Активно' in self.status


    @property
    def status(self):
        text = self.soup.find('span',
                              {'class': 'x8t9es0 xw23nyj xo1l8bm x63nzvj x108nfp6 xq9mrsl x1h4wwuj xeuugli x1i64zmx'})
        if text:
            return text.text
        return ''

    @property
    def org_name(self):
        span = self.soup.find('span',
                              {'class': 'x8t9es0 x1fvot60 xxio538 x108nfp6 xq9mrsl x1h4wwuj x117nqv4 xeuugli'})
        if span:
            return span.text
        return ''
    @property
    def org_link(self):
        a = self.soup.find('a', {'class': 'xt0psk2 x1hl2dhg xt0b8zv x8t9es0 x1fvot60 xxio538 xjnfcd9 xq9mrsl x1yc453h x1h4wwuj x1fcty0u'})
        if a:
            try:
                return a['href']
            except KeyError:
                return ''
        return ''
    @property
    def ads_id(self):
        info_block = self.soup.find('div', {'class': 'xeuugli x2lwn1j x1cy8zhl x78zum5 x1qughib xh8yej3 xxx'})
        if info_block:
            lines = info_block.find_all('div', {'class': 'x3nfvp2 x1e56ztr'})
            if lines:
                id_block = lines[0]
                if 'Библиотеки' in id_block.text:
                    return ''.join(filter(lambda char:char.isdigit(), id_block.text))
        return ''

    @property
    def ads_time(self):
        lines = self.soup.find_all('div',
                              {'class': 'x3nfvp2 x1e56ztr'})
        if lines and len(lines) >=3:
            time_block = lines[2]
            span = time_block.find('span',
                                  {'class': 'x8t9es0 xw23nyj xo1l8bm x63nzvj x108nfp6 xq9mrsl x1h4wwuj xeuugli'})
            if span:
                return span.text
        return ''

    def _get_fields(self):
        return (self.status, self.org_name, self.org_link, self.ads_time)

    def print(self):
        print('\n[Card] ******************')
        print('ID Библиотеки:', self.ads_id)
        print('Status:', self.status)
        print('Org:', self.org_name)
        print('Link:', self.org_link)
        print('Time:', self.ads_time)

class CardSearch:

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')


    def __call__(self):
        block_class = 'xxx'
        cards = self.soup.select(f'div.xrvj5dj.xdq2opy.xexx8yu.xbxaen2.x18d9i69.xbbxn1n.xdoe023.xbumo9q.x143o31f.x7sq92a.x1crum5w > div.xh8yej3:not(.{block_class})')
        cards_class = []
        for card_soup in cards:
            card = Card(card_soup)
            cards_class.append(card)
        print('Cards found', len(cards_class))
        return cards_class


class Cards:

    API_COLLECTOR_URL = 'http://127.0.0.1:8000/ads/groups_update/'

    def __init__(self):
        self.cards = []


    def __getitem__(self, i):
        return self.cards[i]

    def extend(self, seq, log=False):
        self.cards.extend(seq)
        if log:
            print(f'Добавлено в колекцию: {len(seq)}/{len(self)}')

    def __len__(self):
        return len(self.cards)

    def send_to_db(self, clean_after=True, log=False):
        unique_group_urs  = set(card.org_link for card in self)
        group_urls = [{'group_url': group_url} for group_url in unique_group_urs]
        data = {
            'group_urls': group_urls,
        }
        res = req.post(self.API_COLLECTOR_URL, json=data)
        if clean_after:
            self.cards.clear()
        if log:
            print('\n*** Отправка в БД ***')
            print(f'Уникальных: {len(unique_group_urs)} из {len(self)}')
            print('RES:', res.status_code)
            print(res.json())




if __name__ == '__main__':
    with open('fb_site_example/index.html') as file:
        text = file.read()

    with open('fb_site_example/card.html') as file:
        card_text = file.read()

    assert len(text) != 0, 'File Empty!'

    searcher = CardSearch(text)
    find = searcher()
    cards = Cards()
    cards.extend(find)
    for c in cards:
        c.print()
    print(len(cards))