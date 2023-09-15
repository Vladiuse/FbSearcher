from ads.models import FbGroup
from django.test import TestCase
from ads.serializers import FbGroupSerializer
from rest_framework import serializers

class FbGroupSerializerTest(TestCase):

    def test_add_pk(self):
        data = {
            'raw_url': 'http://facebook.com/123123/',
        }

        serializer = FbGroupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer.validated_data['raw_url'],'http://facebook.com/123123/')
        self.assertEqual(serializer.validated_data['id'],'123123')
        serializer.save()
        fb_group = FbGroup.objects.last()
        self.assertEqual(fb_group.pk, '123123')
        self.assertEqual(fb_group.raw_url,'http://facebook.com/123123/')

    def test_raise_url_error(self):
        data = {
            'raw_url': 'http://l.facebook.com/123123/',
        }

        serializer = FbGroupSerializer(data=data)
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_raise_url_no_error(self):
        data = {
            'raw_url': 'http://facebook.com/123123/',
        }

        serializer = FbGroupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        fb_group = FbGroup.objects.get(pk='123123')
        self.assertEqual(fb_group.raw_url, 'http://facebook.com/123123/')


    def test_remove_spaces(self):
        data = {
            'raw_url': 'http://facebook.com/xxx/',
            'email': '  email@email.com  ',
            'name': '  xxx  ',
            'address': '   address  ',
        }

        serializer = FbGroupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        fb_group = FbGroup.objects.get(pk='xxx')
        self.assertEqual(fb_group.email, 'email@email.com')
        self.assertEqual(fb_group.name, 'xxx')
        self.assertEqual(fb_group.address, 'address')


    def test_more_than_255_chars(self):
        data = {
            'raw_url': 'http://facebook.com/xxx/',
            'email': '  email@email.com  ',
            'name': 'xxx' + ' '*280,
            'address': '   address  ',
        }
        serializer = FbGroupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        fb_group = FbGroup.objects.get(pk='xxx')
        self.assertEqual(fb_group.name, 'xxx')

    def test_clean_id(self):
        data = {
            'raw_url': 'http://facebook.com/xxx/',
        }
        serializer = FbGroupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        fb_group = FbGroup.objects.get(pk='xxx')
        self.assertEqual(fb_group.pk, 'xxx')

    def test_clean_id_slash_inside(self):
        data = {
            'raw_url': 'http://facebook.com/xxx/yyy/',
        }
        serializer = FbGroupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        fb_group = FbGroup.objects.get(pk='xxx/yyy')
        self.assertEqual(fb_group.pk, 'xxx/yyy')

    def test_clean_id_no_slash_end(self):
        data = {
            'raw_url': 'http://facebook.com/xxx/yyy',
        }
        serializer = FbGroupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        fb_group = FbGroup.objects.get(pk='xxx/yyy')
        self.assertEqual(fb_group.pk, 'xxx/yyy')






