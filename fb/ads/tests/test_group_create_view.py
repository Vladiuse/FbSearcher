from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from ads.models import FbGroup, FbLibAd



class MassCreateViewTest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('group-list')



