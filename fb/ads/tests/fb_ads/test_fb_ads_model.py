from django.test import TestCase
from ads.models import FbLibAd, FbGroup
from django.core.exceptions import ValidationError


class FbLibAdModelTest(TestCase):

    def test_correct_data_active(self):
        group = FbGroup.objects.create(group_id=1, url='123')
        ad, created = FbLibAd.create_or_update(
            group=group,
            id='1307028233146913',
            status='1',
            time_text='Показ начат 22 дек 2021 г.',
        )
        self.assertEqual(FbLibAd.objects.count(), 1)
        self.assertEqual(group.ads.count(),1)

    def test_correct_data_not_active(self):
        group = FbGroup.objects.create(group_id=1, url='123')
        ad, created = FbLibAd.create_or_update(
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
            ad, created = FbLibAd.create_or_update(
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
            ad, created = FbLibAd.create_or_update(
                group=group,
                id='1307028233146913',
                status='Active',
                time_text='Показ начат 22 дек 2021 г.',
            )
            self.assertEqual(FbLibAd.objects.count(), 1)
            self.assertEqual(group.ads.count(),1)

    def test_alredy_exists(self):
        group = FbGroup.objects.create(group_id=1, url='123')
        ad = FbLibAd.objects.create(group=group, status=FbLibAd.ACTIVE_CODE,id='1307028233146913', time_text='Показ начат 22 дек 2021 г.')
        self.assertEqual(FbLibAd.objects.count(), 1)
        self.assertEqual(FbGroup.objects.count(), 1)
        self.assertEqual(group.ads.count(), 1)

        ad, created =  FbLibAd.create_or_update(group=group, status=FbLibAd.ACTIVE_CODE, id='1307028233146913', time_text='Показ начат 22 дек 2021 г.')
        self.assertEqual(created, False)
        self.assertEqual(FbLibAd.objects.count(), 1)
        self.assertEqual(group.ads.count(), 1)


    def test_update_status_valid(self):
        group = FbGroup.objects.create(group_id=1, url='123')
        ad = FbLibAd.objects.create(group=group, status=FbLibAd.ACTIVE_CODE,id='1307028233146913', time_text='Показ начат 22 дек 2021 г.')
        self.assertEqual(FbLibAd.objects.count(), 1)
        self.assertEqual(FbGroup.objects.count(), 1)
        self.assertEqual(group.ads.count(), 1)

        ad, created =  FbLibAd.create_or_update(group=group, status=FbLibAd.NOT_ACTIVE_CODE, id='1307028233146913', time_text='Показ начат 22 дек 2021 г.')
        self.assertEqual(created, False)
        self.assertEqual(FbLibAd.objects.count(), 1)
        self.assertEqual(group.ads.count(), 1)
        self.assertEqual(ad.status, FbLibAd.NOT_ACTIVE_CODE)

    def test_update_status_in_valid(self):
        group = FbGroup.objects.create(group_id=1, url='123')
        ad = FbLibAd.objects.create(group=group, status=FbLibAd.ACTIVE_CODE,id='1307028233146913', time_text='Показ начат 22 дек 2021 г.')
        self.assertEqual(FbLibAd.objects.count(), 1)
        self.assertEqual(FbGroup.objects.count(), 1)
        self.assertEqual(group.ads.count(), 1)
        with self.assertRaises(ValidationError):
            ad, created =  FbLibAd.create_or_update(group=group, status='xxx', id='1307028233146913', time_text='Показ начат 22 дек 2021 г.')
        self.assertEqual(FbLibAd.objects.count(), 1)
        self.assertEqual(group.ads.count(), 1)
        self.assertEqual(ad.status, FbLibAd.ACTIVE_CODE)


    def test_update_time_text_valid(self):
        group = FbGroup.objects.create(group_id=1, url='123')
        ad = FbLibAd.objects.create(group=group, status=FbLibAd.ACTIVE_CODE,id='1307028233146913', time_text='Показ начат 22 дек 2021 г.')
        self.assertEqual(FbLibAd.objects.count(), 1)
        self.assertEqual(FbGroup.objects.count(), 1)
        self.assertEqual(group.ads.count(), 1)

        ad, created =  FbLibAd.create_or_update(group=group, status=FbLibAd.NOT_ACTIVE_CODE, id='1307028233146913', time_text='New')
        self.assertEqual(created, False)
        self.assertEqual(FbLibAd.objects.count(), 1)
        self.assertEqual(group.ads.count(), 1)
        self.assertEqual(ad.time_text, 'New')

    def test_update_time_text_blank(self):
        group = FbGroup.objects.create(group_id=1, url='123')
        ad = FbLibAd.objects.create(group=group, status=FbLibAd.ACTIVE_CODE,id='1307028233146913', time_text='Показ начат 22 дек 2021 г.')
        self.assertEqual(FbLibAd.objects.count(), 1)
        self.assertEqual(FbGroup.objects.count(), 1)
        self.assertEqual(group.ads.count(), 1)
        with self.assertRaises(ValidationError):
            ad, created =  FbLibAd.create_or_update(group=group, status='xxx', id='1307028233146913', time_text='')
        self.assertEqual(FbLibAd.objects.count(), 1)
        self.assertEqual(group.ads.count(), 1)
        self.assertEqual(ad.time_text, 'Показ начат 22 дек 2021 г.')