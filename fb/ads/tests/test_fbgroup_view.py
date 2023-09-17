from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from ads.models import FbGroup
from django.utils import timezone
from datetime import timedelta



class FbGroupCreateTest(APITestCase):

    def setUp(self) -> None:
        self.update_url = reverse('group-update-list')

    def test_valid_one_item(self):
        data = [
            {'group_url': 'https://facebook.com/123/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(FbGroup.objects.count(),1)


    def test_valid_few_items(self):
        data = [
            {'group_url': 'https://facebook.com/123/'},
            {'group_url': 'https://facebook.com/124/'},
            {'group_url': 'https://facebook.com/125/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(FbGroup.objects.count(),3)

    def test_valid_one_item_invalid(self):
        data = [
            {'group_url': 'https://x.facebook.com/123/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(FbGroup.objects.count(),0)

    def test_valid_few_items_invalid(self):
        data = [
            {'group_url': 'https://x.facebook.com/123/'},
            {'group_url': 'https://x.facebook.com/124/'},
            {'group_url': 'https://x/facebook.com/125/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(FbGroup.objects.count(),0)


    def test_few_valid_few_invalid(self):
        data = [
            {'group_url': 'https://facebook.com/123/'},
            {'group_url': 'https://facebook.com/124/'},
            {'group_url': 'https://x.facebook.com/125/'},
            {'group_url': 'https://x.facebook.com/125/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(FbGroup.objects.count(),2)


class FbGroupUpdateViewTest(APITestCase):

    def setUp(self) -> None:
        self.update_url = reverse('group-update-list')
        self.past_day_7 = timezone.now().date() - timedelta(days=7)
        self.past_day_5 = timezone.now().date() - timedelta(days=5)
        self.past_day_3 = timezone.now().date() - timedelta(days=3)
        self.group_1 = FbGroup.objects.create(group_id=1, last_ad_date=self.past_day_7)
        self.group_2 = FbGroup.objects.create(group_id=2, last_ad_date=self.past_day_5)
        self.group_3 = FbGroup.objects.create(group_id=3, last_ad_date=self.past_day_3)

    def test_no_updates(self):
        data = [
            {'group_url': 'https://facebook.com/123/'},
            {'group_url': 'https://facebook.com/124/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(FbGroup.objects.count(),2 + 3)
        self.assertEqual(self.group_1.last_ad_date, self.past_day_7)
        self.assertEqual(self.group_2.last_ad_date, self.past_day_5)
        self.assertEqual(self.group_3.last_ad_date, self.past_day_3)

    def test_update_one(self):
        data = [
            {'group_url': 'https://facebook.com/123/'},
            {'group_url': 'https://facebook.com/124/'},
            {'group_url': 'https://facebook.com/1/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(FbGroup.objects.count(),2 + 3)
        self.group_1.refresh_from_db()
        self.assertEqual(self.group_1.last_ad_date, timezone.now().date())
        self.assertEqual(self.group_2.last_ad_date, self.past_day_5)
        self.assertEqual(self.group_3.last_ad_date, self.past_day_3)


    def test_update_all(self):
        data = [
            {'group_url': 'https://facebook.com/3/'},
            {'group_url': 'https://facebook.com/2/'},
            {'group_url': 'https://facebook.com/1/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(FbGroup.objects.count(), 3)
        self.group_1.refresh_from_db()
        self.group_2.refresh_from_db()
        self.group_3.refresh_from_db()
        self.assertEqual(self.group_1.last_ad_date, timezone.now().date())
        self.assertEqual(self.group_2.last_ad_date, timezone.now().date())
        self.assertEqual(self.group_3.last_ad_date, timezone.now().date())



class FbGroupViewResTest(APITestCase):
    def setUp(self) -> None:
        self.update_url = reverse('group-update-list')

    def test_no_data(self):
        data = []
        res = self.client.post(self.update_url, data=data, format='json')
        correct_response = {
            'invalid_data': [],
            'invalid_count': 0,
            'total': 0,
            'new': 0,
        }
        self.assertEqual(res.data, correct_response)

    def test_one_valid_new(self):
        data = [
            {'group_url': 'https://facebook.com/1/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        correct_response = {
            'invalid_data': [],
            'invalid_count': 0,
            'total': 1,
            'new': 1,
        }
        self.assertEqual(res.data, correct_response)

    def test_one_valid_not_new(self):
        FbGroup.objects.create(group_id=1)
        data = [
            {'group_url': 'https://facebook.com/1/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        correct_response = {
            'invalid_data': [],
            'invalid_count': 0,
            'total': 1,
            'new': 0,
        }
        self.assertEqual(res.data, correct_response)


    def test_one_invalid_new(self):
        data = [
            {'group_url': 'https://x.facebook.com/1/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        correct_response = {
            'invalid_data': [ {'group_url': 'https://x.facebook.com/1/'}],
            'invalid_count': 1,
            'total': 1,
            'new': 0,
        }
        self.assertEqual(res.data, correct_response)


    def test_few_valid_new(self):
        data = [
            {'group_url': 'https://facebook.com/1/'},
            {'group_url': 'https://facebook.com/3/'},
            {'group_url': 'https://facebook.com/2/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        correct_response = {
            'invalid_data': [],
            'invalid_count': 0,
            'total': 3,
            'new': 3,
        }
        self.assertEqual(res.data, correct_response)


    def test_few_valid_one_update(self):
        FbGroup.objects.create(group_id=1)
        data = [
            {'group_url': 'https://facebook.com/1/'},
            {'group_url': 'https://facebook.com/3/'},
            {'group_url': 'https://facebook.com/2/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        correct_response = {
            'invalid_data': [],
            'invalid_count': 0,
            'total': 3,
            'new': 2,
        }
        self.assertEqual(res.data, correct_response)


    def test_few_valid_one_invalid(self):
        data = [
            {'group_url': 'https://facebook.com/1/'},
            {'group_url': 'https://facebook.com/3/'},
            {'group_url': 'https://x.facebook.com/2/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        correct_response = {
            'invalid_data': [ {'group_url': 'https://x.facebook.com/2/'},],
            'invalid_count': 1,
            'total': 3,
            'new': 2,
        }
        self.assertEqual(res.data, correct_response)


    def test_few_valid_one_invalid_one_update(self):
        FbGroup.objects.create(group_id=1)
        data = [
            {'group_url': 'https://facebook.com/1/'},
            {'group_url': 'https://facebook.com/2/'},
            {'group_url': 'https://facebook.com/3/'},
            {'group_url': 'https://x.facebook.com/20/'},
        ]
        res = self.client.post(self.update_url, data=data, format='json')
        correct_response = {
            'invalid_data': [ {'group_url': 'https://x.facebook.com/20/'},],
            'invalid_count': 1,
            'total': 4 ,
            'new': 2,
        }
        self.assertEqual(res.data, correct_response)



