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
        info_block = self.soup.find('div', {'class': 'xeuugli x2lwn1j x1cy8zhl x78zum5 x1qughib xh8yej3'})
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
        self.cards = self._get_cards_from_html()

    def _get_cards_from_html(self):
        cards = self.soup.select(f'div.xrvj5dj.xdq2opy.xexx8yu.xbxaen2.x18d9i69.xbbxn1n.xdoe023.xbumo9q.x143o31f.x7sq92a.x1crum5w > div.xh8yej3')
        cards_class = []
        for card_soup in cards:
            card = Card(card_soup)
            cards_class.append(card)
        return cards_class

    @property
    def links(self):
        return [card.org_link for card in self.cards]



if __name__ == '__main__':
    with open('/home/vlad/PycharmProjects/FbSearcher/log.html') as file:
        html = file.read()
        searcher = CardSearch(html)
        links = searcher.links
        print(links)

