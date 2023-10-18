import unittest
from ads.fbgroup_link_parser import get_fbgroup_id_from_url



class FbGroupUrlParserTest(unittest.TestCase):

    def test_no_https_valid(self):
        url = 'http://facebook.com/123123/'
        result = get_fbgroup_id_from_url(url)
        self.assertEqual(result, '123123')

    def test_no_slash_in_end(self):
        url = 'http://facebook.com/123123'
        result = get_fbgroup_id_from_url(url)
        self.assertEqual(result, '123123')

    def test_www_in_link(self):
        url = 'http://www.facebook.com/123123'
        result = get_fbgroup_id_from_url(url)
        self.assertEqual(result, '123123')

    def test_page_in_link(self):
        url = 'http://fb.com/page-123123'
        result = get_fbgroup_id_from_url(url)
        self.assertEqual(result, '123123')

    def test_id_with_letters(self):
        url = 'http://facebook.com/asdasdasd/'
        result = get_fbgroup_id_from_url(url)
        self.assertEqual(result, 'asdasdasd')

    def test_id_with_diff_chars(self):
        url = 'http://facebook.com/asda-=_.123Adasd/'
        result = get_fbgroup_id_from_url(url)
        self.assertEqual(result, 'asda-=_.123Adasd')


    def test_few_all_valid_only_numbers(self):
        urls = [
            'http://facebook.com/123123123123',
            'https://facebook.com/123123123123',

            'http://facebook.com/123123123123/',
            'https://facebook.com/123123123123/',

            'http://www.facebook.com/123123123123/',
            'https://www.facebook.com/123123123123/',

            'http://www.facebook.com/123123123123',
            'https://www.facebook.com/123123123123',
        ]
        for url in urls:
            result = get_fbgroup_id_from_url(url)
            self.assertEqual(result, '123123123123')


    def test_few_all_valid_chars(self):
        urls = [
            'http://facebook.com/asd123-_.ASD',
            'http://facebook.com/asd123-_.ASD',

            'https://facebook.com/asd123-_.ASD',
            'https://facebook.com/asd123-_.ASD',

            'https://facebook.com/asd123-_.ASD/',
            'https://facebook.com/asd123-_.ASD/',

            'http://www.facebook.com/asd123-_.ASD',
            'http://www.facebook.com/asd123-_.ASD',

            'https://www.facebook.com/asd123-_.ASD',
            'https://www.facebook.com/asd123-_.ASD',

            'https://www.facebook.com/asd123-_.ASD/',
            'https://www.facebook.com/asd123-_.ASD/',
        ]
        for url in urls:
            result = get_fbgroup_id_from_url(url)
            self.assertEqual(result, 'asd123-_.ASD', msg=url)

    def test_all_valid_page_in_url(self):
        urls = [
            'http://fb.com/page-123123123123',
            'https://fb.com/page-123123123123',

            'http://fb.com/page-123123123123/',
            'https://fb.com/page-123123123123/',

            'http://www.fb.com/page-123123123123/',
            'https://www.fb.com/page-123123123123/',

            'http://www.fb.com/page-123123123123',
            'https://www.fb.com/page-123123123123'
        ]
        for url in urls:
            result = get_fbgroup_id_from_url(url)
            self.assertEqual(result, '123123123123')

    def test_not_valid(self):
        urls = [
            'https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.instagram.com%2F_u%2Flongislandleafguard&h=AT2dBzGWHTAFtJjpVcaSSvPAgebSvTBOm4ZNBoQxj62qEYulgaOfd4r_9t5Pul3UVWXhvgz2Uw5CDmHA7ZbpXYc71-PcyW5HgSgh37yYa0x4_WLSWzCzRezpDlknf6yn-m0IuJQFR7q2pg',
            'https://instagram/asdoem',
        ]
        for url in urls:
            result = get_fbgroup_id_from_url(url)
            self.assertEqual(result, '')