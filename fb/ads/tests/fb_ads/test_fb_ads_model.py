from django.test import TestCase
from ads.models import FbLibAd, FbGroup
from django.core.exceptions import ValidationError


class FbLibAdModelTest(TestCase):

    def test_correct_data_active(self):
        group = FbGroup.objects.create(group_id=1, url='123')
        ad, created = FbLibAd.get_or_create(
            group=group,
            id='1307028233146913',
            status='1',
            time_text='Показ начат 22 дек 2021 г.',
        )
        self.assertEqual(FbLibAd.objects.count(), 1)
        self.assertEqual(group.ads.count(),1)

    def test_correct_data_not_active(self):
        group = FbGroup.objects.create(group_id=1, url='123')
        ad, created = FbLibAd.get_or_create(
            group=group,
            id='1307028233146913',
            status='0',
            time_text='Показ начат 22 дек 2021 г.',
        )
        self.assertEqual(FbLibAd.objects.count(), 1)
        self.assertEqual(group.ads.count(),1)

    def test_not_valid_ads_id(self):
        group = FbGroup.objects.create(group_id=1, url='123')
        with self.assertRaises(ValueError):
            ad, created = FbLibAd.get_or_create(
                group=group,
                id='1307028233146913asd',
                status='0',
                time_text='Показ начат 22 дек 2021 г.',
            )
            self.assertEqual(FbLibAd.objects.count(), 1)
            self.assertEqual(group.ads.count(),1)

    def test_not_valid_status(self):
        group = FbGroup.objects.create(group_id=1, url='123')
        with self.assertRaises(ValidationError):
            ad, created = FbLibAd.get_or_create(
                group=group,
                id='1307028233146913',
                status='Active',
                time_text='Показ начат 22 дек 2021 г.',
            )
            self.assertEqual(FbLibAd.objects.count(), 1)
            self.assertEqual(group.ads.count(),1)
