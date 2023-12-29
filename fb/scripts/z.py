from ads.models import FbGroup
from django.db.models import Count
from django.utils import timezone
import csv


FbGroup.log_data()

# # PROPARSE AGAIN
#qs = FbGroup.objects.filter(created='2023-11-10').filter(email="")
#
#print(qs.count())
#qs.update(status=FbGroup.NOT_LOADED)
