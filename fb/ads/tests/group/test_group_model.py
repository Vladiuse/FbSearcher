from ads.models import FbGroup
from django.test import TestCase
from django.core.exceptions import ValidationError


class FbGroupSerializerTest(TestCase):

    def test_save_valid_url(self):
        url = 'https://facebook.com/123'
        group, created = FbGroup.get_or_create(url=url)
        self.assertEqual(FbGroup.objects.count(), 1)
        fb_group = FbGroup.objects.get(pk='123')
        self.assertEqual(fb_group.pk, '123')

    def test_save_valid_url_no_s(self):
        url = 'http://facebook.com/123'
        group, created = FbGroup.get_or_create(url=url)
        self.assertEqual(FbGroup.objects.count(), 1)
        fb_group = FbGroup.objects.get(pk='123')
        self.assertEqual(fb_group.pk, '123')

    def test_invalid_url_no_path(self):
        url = 'https://facebook.com'
        with self.assertRaises(ValidationError):
            group, created = FbGroup.get_or_create(url=url)

    def test_invalid_url_no_path_spash(self):
        url = 'https://facebook.com/'
        with self.assertRaises(ValidationError):
            group, created = FbGroup.get_or_create(url=url)

    def test_invalid_url_some_sub_domain(self):
        url = 'https://x.facebook.com'
        with self.assertRaises(ValidationError):
            group, created = FbGroup.get_or_create(url=url)

    def test_long_url(self):
        url = 'https://x.facebook.com/123' + 'x'*200
        with self.assertRaises(ValidationError):
            group, created = FbGroup.get_or_create(url=url)
