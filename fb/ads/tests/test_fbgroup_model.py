from django.test import TestCase
from ads.models import FbGroup
from rest_framework.validators import ValidationError
from django.utils import timezone
from datetime import timedelta