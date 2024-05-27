from ads.models import FbGroup
from django.test import TestCase
import unittest


class TestFollowersStringToIntTest(unittest.TestCase):

    def test_main(self):
        DATA = (
            ('0', 0),
            ('1', 1),
            ('12', 12),
            ('122', 122),
            ('1K', 1000),
            ('1.2K', 1200),
            ('1.21K', 1210),
            ('221K', 221000),

            ('1k', 1000),
            ('1.2k', 1200),
            ('1.21k', 1210),
            ('221k', 221000),

            ('1M', 1000 * 1000),
            ('1.2M', 1200 * 1000),
            ('1.21M', 1210 * 1000),
            ('221M', 221000 * 1000),

            ('1m', 1000 * 1000),
            ('1.2m', 1200 * 1000),
            ('1.21m', 1210 * 1000),
            ('221m', 221000 * 1000),
        )
        for followers_string, int_expected in DATA:
            result = FbGroup.followers_to_int(followers_string)
            msg = f'followers_string "{followers_string}" munst be ecual {int_expected}, not {result}'
            self.assertEqual(result, int_expected, msg=msg)

    def test_empty_string(self):
        self.assertIsNone(FbGroup.followers_to_int(''))


    def test_incorrect_chars(self):
        data = (
            '10A',
            '10X',
            '10D',
        )
        for followers in data:
            with self.assertRaises(ValueError):
                FbGroup.followers_to_int(followers)

class ConvertFollowersWhenSaveTest(TestCase):

    def test_no_followers(self):
        group = FbGroup.objects.create(group_id='123',)
        self.assertIsNone(group.followers_int)

    def test_add_int(self):
        DATA = (
            ('0', 0),
            ('1', 1),
            ('12', 12),
            ('122', 122),
            ('1K', 1000),
            ('1.2K', 1200),
            ('1.21K', 1210),
            ('221K', 221000),
            ('1M', 1000 * 1000),
            ('1.2M', 1200 * 1000),
            ('1.21M', 1210 * 1000),
            ('221M', 221000 * 1000),

        )
        for followers_str, int_res in DATA:
            group = FbGroup.objects.create(group_id=followers_str, followers=followers_str)
            self.assertEqual(group.followers_int, int_res)

