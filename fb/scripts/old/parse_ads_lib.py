from parsers import FbLibPage , CardSearch, Cards
from ads.models import KeyWord

key_words = KeyWord.objects.exclude(word='rest')
COUNTRY = 'US'
DATE = '2023-09-17'

cards = Cards()
#TODO check is server run
for num,key_word in enumerate(key_words):
    print(key_word, f'{num+1} из {len(key_words)}')
    q_key = key_word.word
    fb_page = FbLibPage(q=key_word, start_date=DATE, country=COUNTRY)
    try:
        fb_page.open()
        for page in fb_page:
            card_searcher = CardSearch(page)
            find_cards = card_searcher()
            cards.extend(find_cards)
            cards.send_to_db()
        fb_page.close()
    except Exception as error:
        print(error)

