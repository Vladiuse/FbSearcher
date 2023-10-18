from parsers import Cards, FbLibPage, CardSearch

KEY_WORDS_RU = [
    'our','we','that','now','name','male']
cards = Cards()
fb_page = FbLibPage(q='', start_date='2023-10-16', country='US')
input('Wait some: ')
for key_word in KEY_WORDS_RU:
    try:
        fb_page.q = key_word
        fb_page.open()
        print(key_word, fb_page.pages_count)
        for page in fb_page:
            card_searcher = CardSearch(page)
            find_cards = card_searcher()
            cards.extend(find_cards)
            cards.send_to_db()
        fb_page.close()
    except Exception as error:
        print(key_word, 'ERROR', error)