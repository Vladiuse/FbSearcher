from django.test import TestCase
from ads.models import KeyWord
import uuid


class KeyWordTest(TestCase):

    def setUp(self):
        self.numbers_to_create = [
            1, 2, 3, 1000,
            1001, 1002, 1003, 2000,
            2001, 2002, 2003, 3000,
            3001, 3002, 3003, 4000,
            4001, 4002, 4003, 5000,
            5001, 5002, 5003, 6000,
        ]
        self._create_keywords()

    def _create_keywords(self):
        words = [
            KeyWord(number_in_dict=i, word='aa' + str(i)) for i in self.numbers_to_create
        ]
        KeyWord.objects.bulk_create(words)

    def test_func(self):
        self.assertEqual(KeyWord.objects.count(), 24)

    def test_bunch_incorrect_k(self):
        with self.assertRaises(ValueError):
            bunch = KeyWord.get_bunch(k=0)
        with self.assertRaises(ValueError):
            bunch = KeyWord.get_bunch(k=-1)
        with self.assertRaises(ValueError):
            bunch = KeyWord.get_bunch(k=10)

    def test_bunch_incorrect_count(self):
        with self.assertRaises(ValueError):
            bunch = KeyWord.get_bunch(k=2, length=0)
        with self.assertRaises(ValueError):
            bunch = KeyWord.get_bunch(k=2, length=1000)

    def test_no_words_in_qs(self):
        with self.assertRaises(KeyWord.DoesNotExist):
            bunch = KeyWord.get_bunch(k=7)

    def test_mark_collected(self):
        bunch = KeyWord.get_bunch(k=1)
        self.assertTrue(all(item.is_collected for item in bunch))
        self.assertEqual(KeyWord.objects.filter(is_collected=True).count(), 4)
        for key_word in [1,2,3,1000]:
            key = KeyWord.objects.get(word='aa' + str(key_word))
            self.assertTrue(key.is_collected)

    def test_correct_items(self):
        for k in range(1, 6):
            bunch = KeyWord.get_bunch(k=k)
            self.assertEqual(bunch.count(), 4,)
            numbers = [item.number_in_dict for item in bunch]
            expected = self.numbers_to_create[(k-1)*4: (k-1)*4+4]
            self.assertEqual(numbers, expected)

    def test_count(self):
        bunch = KeyWord.get_bunch(k=1, length=1)
        expected_word  = KeyWord.objects.get(word='aa1')
        self.assertTrue(expected_word in bunch)
        self.assertEqual(bunch.count(),1)

    def test_mark_item_collected(self):
        bunch = KeyWord.get_bunch(k=1, length=1)
        expected_word = KeyWord.objects.get(word='aa1')
        self.assertTrue(bunch[0].is_collected)
        self.assertTrue(expected_word in bunch)
        self.assertEqual(KeyWord.objects.filter(is_collected=True).count(),1)
        self.assertEqual(KeyWord.objects.filter(is_collected=False).count(), 23)


    def test_all_collected(self):
        KeyWord.objects.update(is_collected=True)
        with self.assertRaises(KeyWord.DoesNotExist):
            bunch = KeyWord.get_bunch(k=1, length=1)

    def test_length_more_than_items_in_db(self):
        try:
            KeyWord.get_bunch(k=1, length=100)
        except:
            self.fail('Raise some exception')


