from unittest import TestCase
from parsers import FbGroupPage, FbGroupPageNoAuth

class TestGetMail(TestCase):

    def test_find_mail_in_html(self):
        code = """
<div
    class="x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1nhvcw1 x1qjc9v5 xozqiw3 x1q0g3np xyamay9 xykv574 xbmpl8g x4cne27 xifccgj">
    <div class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xsyo7zv x16hj40l x10b6aqq x1yrsyyn">
        <img class="x1b0d499 xuo83w3" src="https://static.xx.fbcdn.net/rsrc.php/v3/yE/r/2PIcyqpptfD.png" alt=""
            height="20" width="20"></div>
    <div
        class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x193iq5w xeuugli x1r8uery x1iyjqo2 xs83m0k xamitd3 xsyo7zv x16hj40l x10b6aqq x1yrsyyn">
        <div class="x78zum5 xdt5ytf xz62fqu x16ldp7u">
            <div class="xu06os2 x1ok221b"><span
                    class="x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"
                    dir="auto">manager@polsza.info</span></div>
        </div>
    </div>
</div>        
"""
        page = FbGroupPage(code)
        expected = 'manager@polsza.info'
        result = page.get_group_email_from_html_block()
        self.assertEqual(result, expected)

    def test_no_mail_in_html(self):
        code = """ """
        page = FbGroupPage(code)
        result = page.get_group_email_from_html_block()
        self.assertEqual(result, None)




class FbGroupNoAuthTestEmail(TestCase):

    def test_get_email_by_regex_no_email(self):
        code = """ """
        page = FbGroupPageNoAuth(code)
        result = page._get_email_by_regex()
        self.assertEqual(result, None)

    def test_get_email_by_regex_email_exists(self):
        code = """Найти мыло в коде (елси незалогинен)
              Пример: "text":"someemail@gmail.com" dasda
              """
        page = FbGroupPageNoAuth(code)
        result = page._get_email_by_regex()
        self.assertEqual(result, 'someemail@gmail.com')

    def test_get_email_by_regex_email_exists_2(self):
        code = """Найти мыло в коде (елси незалогинен)
              Пример: "text":"someemail\\u0040gmail.com" dasda
              """
        page = FbGroupPageNoAuth(code)
        result = page._get_email_by_regex()
        self.assertEqual(result, 'someemail@gmail.com')

    def test_get_email_by_regex_email_clean_code_1(self):
        code = """Найти мыло в коде (елси незалогинен)
              Пример: "text":"someemail@gmail.com" dasda
              """
        page = FbGroupPageNoAuth(code)
        result = page._get_email_by_regex()
        self.assertEqual(result, 'someemail@gmail.com')
        for string in ('"', '"text"', ':', ' '):
            self.assertTrue(string not in result)

    def test_get_email_by_regex_email_clean_code_2(self):
        code = """Найти мыло в коде (елси незалогинен)
              Пример: "text":"someemail\\u0040gmail.com" dasda
              """
        page = FbGroupPageNoAuth(code)
        result = page._get_email_by_regex()
        self.assertEqual(result, 'someemail@gmail.com')
        for string in ('"', '"text"', ':', ' '):
            self.assertTrue(string not in result)

    def test_get_email(self):
        code = """Найти мыло в коде (елси незалогинен)
              Пример: "text":"someemail\\u0040gmail.com" dasda
              """
        page = FbGroupPageNoAuth(code)
        result = page.get_email()
        self.assertEqual(result, 'someemail@gmail.com')



class FbGroupNoAuthTestName(TestCase):

    def test_no_title(self):
        code = ''
        page = FbGroupPageNoAuth(code)
        res = page._get_name_from_title()
        self.assertIsNone(res)

    def test_title_exists(self):
        code = """
        <title>xxx</title>
        """
        page = FbGroupPageNoAuth(code)
        res = page._get_name_from_title()
        self.assertEqual(res, 'xxx')

    def test_clean_title_one(self):
        code = """
        <title>xxx| yyy</title>
        """
        page = FbGroupPageNoAuth(code)
        res = page._get_name_from_title()
        self.assertEqual(res, 'xxx')

    def test_clean_title_few(self):
        code = """
        <title>xxx| yyy | zzz</title>
        """
        page = FbGroupPageNoAuth(code)
        res = page._get_name_from_title()
        self.assertEqual(res, 'xxx')

    def test_get_name(self):
        code = """
        <title>xxx| yyy | zzz</title>
        """
        page = FbGroupPageNoAuth(code)
        res = page.get_name()
        self.assertEqual(res, 'xxx')


class FbGroupNoAuthTest(TestCase):

    def test_call(self):
        code = """
        <title>xxx| yyy | zzz</title>
        Найти мыло в коде (елси незалогинен)
              Пример: "text":"someemail\\u0040gmail.com" dasda
        """
        page = FbGroupPageNoAuth(code)
        page()
        self.assertTrue(page.name, 'xxx')
        self.assertTrue(page.email, 'someemail@gmail.com')

    def test_get_result_no_data(self):
        code = """
        """
        page = FbGroupPageNoAuth(code)
        page()
        self.assertEqual(page.result, {})

    def test_get_result_no_email(self):
        code = """
                <title>xxx| yyy | zzz</title>
        """
        page = FbGroupPageNoAuth(code)
        page()
        self.assertEqual(page.result['name'], 'xxx')
        self.assertTrue('email' not in page.result)

    def test_get_result_no_name(self):
        code = """
                     Найти мыло в коде (елси незалогинен)
              Пример: "text":"someemail\\u0040gmail.com" dasda
        """
        page = FbGroupPageNoAuth(code)
        page()
        self.assertEqual(page.result['email'], 'someemail@gmail.com')
        self.assertTrue('name' not in page.result)

    def test_not_call_before_result(self):
        code = """
                     Найти мыло в коде (елси незалогинен)
              Пример: "text":"someemail\\u0040gmail.com" dasda
        """
        page = FbGroupPageNoAuth(code)
        with self.assertRaises(AttributeError):
            page.result

class FbGroupNoAuthTestFollowers(TestCase):


    def test_no_followers(self):
        code = ""
        page = FbGroupPageNoAuth(code)
        page()
        self.assertIsNone(page.followers)

    def test_get_followers_from_code(self):
        code = ""
        page = FbGroupPageNoAuth(code)
        followers = page._get_followers_from_code()
        self.assertIsNone(followers)

    def test_get_followers(self):
        code = ""
        page = FbGroupPageNoAuth(code)
        page.get_followers()
        self.assertIsNone(page.followers)

    def test_followers_exists_no_K(self):
        code = """
        "inline_style":"BOLD"}],"aggregated_ranges":[],"ranges":[],
        "color_ranges":[],"text":"769 followers"},"uri":"https:\/\/www.facebook.com\/BarelyBrokeLA\/followers\/"}],
        """
        page = FbGroupPageNoAuth(code)
        page()
        self.assertEqual(page.followers, '769')

    def test_followers_K_exists(self):
        code = """
        "inline_style":"BOLD"}],"aggregated_ranges":[],"ranges":[],
        "color_ranges":[],"text":"2.9K followers"},"uri":"https:\/\/www.facebook.com\/BarelyBrokeLA\/followers\/"}],
        """
        page = FbGroupPageNoAuth(code)
        page()
        self.assertEqual(page.followers, '2.9K')

    def test_followers_K_exists_no_point(self):
        code = """
        "inline_style":"BOLD"}],"aggregated_ranges":[],"ranges":[],
        "color_ranges":[],"text":"29K followers"},"uri":"https:\/\/www.facebook.com\/BarelyBrokeLA\/followers\/"}],
        """
        page = FbGroupPageNoAuth(code)
        page()
        self.assertEqual(page.followers, '29K')

    def test_followers_K_exists_small(self):
        code = """
        "inline_style":"BOLD"}],"aggregated_ranges":[],"ranges":[],
        "color_ranges":[],"text":"2.9k followers"},"uri":"https:\/\/www.facebook.com\/BarelyBrokeLA\/followers\/"}],
        """
        page = FbGroupPageNoAuth(code)
        page()
        self.assertEqual(page.followers, '2.9k')

    def test_followers_M_exists_small(self):
        code = """
        "inline_style":"BOLD"}],"aggregated_ranges":[],"ranges":[],
        "color_ranges":[],"text":"3.3m followers"},"uri":"https:\/\/www.facebook.com\/BarelyBrokeLA\/followers\/"}],
        """
        page = FbGroupPageNoAuth(code)
        page()
        self.assertEqual(page.followers, '3.3m')

    def test_followers_M_exists(self):
        code = """
        "inline_style":"BOLD"}],"aggregated_ranges":[],"ranges":[],
        "color_ranges":[],"text":"3.3M followers"},"uri":"https:\/\/www.facebook.com\/BarelyBrokeLA\/followers\/"}],
        """
        page = FbGroupPageNoAuth(code)
        page()
        self.assertEqual(page.followers, '3.3M')

    def test_bunch(self):
        examples = [
            '111',
            '1k',
            '2.2k',
            '22.2k',
            '222.2k',
            '2.21k',
            '2.213k',
            #
            '1K',
            '2.2K',
            '22.2K',
            '222.2K',
            '2.21K',
            '2.212K',
            #
            '1m',
            '2.2m',
            '22.2m',
            '222.2m',
            '2.21m',
            '2.212m',
            #
            '1M',
            '2.2M',
            '22.2M',
            '222.2M',
            '2.21M',
            '2.212M',
        ]
        for i in examples:
            code = f'"color_ranges":[],"text":"{i} followers","uri":"https:'
            page = FbGroupPageNoAuth(code)
            page()
            self.assertEqual(page.followers, i)

    def test_followers_in_result(self):
        code = """
        "inline_style":"BOLD"}],"aggregated_ranges":[],"ranges":[],
        "color_ranges":[],"text":"2.9k followers"},"uri":"https:\/\/www.facebook.com\/BarelyBrokeLA\/followers\/"}],
        """
        page = FbGroupPageNoAuth(code)
        page()
        result = page.result
        self.assertEqual(result['followers'], '2.9k')

    def test_followers_not_in_result(self):
        code = ""
        page = FbGroupPageNoAuth(code)
        page()
        result = page.result
        self.assertTrue('followers' not in result)





