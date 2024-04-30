from ads.models import FbGroup
from datetime import datetime
import csv

updates_border_date = datetime.strptime(FbGroup.UPDATE_BORDER_DATE, '%Y-%m-%d').date()
def create_file():
    FILE_SIZE = 999
    print('File Size', FILE_SIZE)
    res = input('you shore?: ', )
    if res.lower() not in ['y', 'yes']:
        raise KeyError
    
    for i in range(10,20):
        used_count = 2
        # NEW
        #qs = FbGroup.download_objects.filter(used_count=0)[:FILE_SIZE] # for new
        # USED
        qs = FbGroup.download_objects.filter(last_ad_date__gte=updates_border_date).filter(used_count=used_count)[:FILE_SIZE] # for updatet data
        # CORP
        #qs = FbGroup.download_objects.filter(used_count=2).filter(email_service_id__isnull=True)[:FILE_SIZE]  # korporat
        qs_list = list(qs)
        print(i, len(qs_list))
        if len(qs_list) != FILE_SIZE:
            raise ValueError('Data ends')
        groups_to_update = []
        with open(f'/home/vlad/csv_reports/{i}.csv', 'w', newline='\n') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"')
            for group in qs_list:
                writer.writerow([group.name, group.email])
                groups_to_update.append(group.pk)
        qs = FbGroup.objects.filter(pk__in=groups_to_update)
        qs.update(used_count=3)
    return '/home/vlad/all.csv'

create_file()


# NEW corps
#print(FbGroup.download_objects.filter(last_ad_date__gte=updates_border_date).filter(used_count=0).filter(
 #            email_service_id__isnull=True).count())
