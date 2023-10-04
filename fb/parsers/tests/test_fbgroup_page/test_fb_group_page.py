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






