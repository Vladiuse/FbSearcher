from django.test import TestCase
from ads.models import FbGroup
from ads.serializers import FbGroupCreateSerializer
from rest_framework.validators import ValidationError
from django.utils import timezone
from datetime import timedelta

class FbGroupSerializerTest(TestCase):

    def test_valid_data(self):
        data = {
            'group_url': 'https://facebook.com/123/',
        }
        serializer = FbGroupCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(FbGroup.objects.count(),1)

    def test_valid_data_alredy_exists(self):
        FbGroup.objects.create(group_id='123')
        self.assertEqual(FbGroup.objects.count(), 1)
        data = {
            'group_url': 'https://facebook.com/123/',
        }
        serializer = FbGroupCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(FbGroup.objects.count(), 1)


    def test_invalid_data(self):
        data = {
            'group_url': 'https://x.facebook.com/123/',
        }
        serializer = FbGroupCreateSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
            serializer.save()
        self.assertEqual(FbGroup.objects.count(),0)


    def test_update_ad_last_date(self):
        delta = timedelta(days=7)
        start_date = timezone.now().date() - delta
        group = FbGroup.objects.create(group_id='123', last_ad_date=start_date)
        self.assertEqual(group.last_ad_date, timezone.now().date() - delta)

        data = {
            'group_url': 'https://facebook.com/123/',
        }
        serializer = FbGroupCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save()
        self.assertEqual(group.group_id, '123')
        self.assertEqual(group.last_ad_date, timezone.now().date())

