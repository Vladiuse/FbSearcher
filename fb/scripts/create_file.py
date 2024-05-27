import os.path

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

    for i in range(70,75):
        used_count = 2
        # NEW
        qs = FbGroup.download_objects.filter(used_count=0)[:FILE_SIZE]  # for new
        # USED
        #qs = FbGroup.download_objects.filter(last_ad_date__gte=updates_border_date).filter(used_count=used_count)[
             #:FILE_SIZE]  # for updatet data
        # CORP
        # qs = FbGroup.download_objects.filter(used_count=0).filter(email_service_id__isnull=True)[:FILE_SIZE]  # korporat
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





class FileGroupDrawer:
    FILE_SIZE = 1000
    TESTS_COUNT = 1
    USED_COUNT = 1

    ROOT = '/home/vlad/csv_reports'

    def __init__(self):
        self.queries = []

    @property
    def file_size(self):
        return self.FILE_SIZE - self.TESTS_COUNT

    def info(self):
        print('FileGroupDrawer info:')
        for qs in self.queries:
            print(qs)

    def _get_all_groups_ids(self):
        groups_ids = list()
        for file_qs in self.queries:
            for group in file_qs.qs:
                groups_ids.append(group.pk)
        return groups_ids

    def _check_is_all_groups_unique(self):
        total_count = sum([len(qs) for qs in self.queries])
        unique_groups_ids = set(self._get_all_groups_ids())
        if len(unique_groups_ids) != total_count:
            raise ValueError(f'Есть преречение qs: Всего - {total_count}, уникальных - {len(unique_groups_ids)}')
        else:
            print('Qss not have duplicated')

    def create_file_qss(self, *, new_data_count=0, used_data_count=0, split_corps=False, ):
        _map = (
            ('new', new_data_count, 0),
            (f'used', used_data_count, FileGroupDrawer.USED_COUNT),
        )
        for type, files_count, used_count in _map:
            if files_count:
                if not split_corps:
                    file_g_query = FileGroupQuery(type, files_count, self)
                    self.queries.append(file_g_query)
                else:
                    not_corp_files_count = int(files_count / 2)
                    if files_count % 2 == 0:
                        corp_files_count = int(files_count / 2)
                    else:
                        corp_files_count = int(files_count / 2) + 1
                    file_corp_qs = FileGroupQuery(type + '_corp', corp_files_count, self)
                    file_not_corp_qs = FileGroupQuery(type + '_not_corp', not_corp_files_count, self)
                    self.queries.append(file_corp_qs)
                    self.queries.append(file_not_corp_qs)

        self._check_is_all_groups_unique()

    def _get_file_number(self):
        exiting_files = list(filter(lambda file_name: file_name.endswith('csv'), os.listdir(self.ROOT)))
        if not exiting_files:
            return 0
        numbers = list()
        for file_name in exiting_files:
            filename, ext = os.path.splitext(file_name)
            if filename.isdigit():
                numbers.append(int(filename))
        return max(numbers) + 1

    def create_files(self, ):
        res = input('Start creating files?: ', )
        if res.lower() not in ['y', 'yes']:
            raise exit()
        for qs in self.queries:
            print(f'Create files for {qs.qs_type}')
            groups = iter(qs.qs)
            for _ in range(qs.files_count):
                file_name = f'{self._get_file_number()}.csv'
                file_path = os.path.join(self.ROOT, file_name)
                if os.path.exists(file_path):
                    raise ValueError(f'File {file_path} already exists')
                print(f'- create file {file_name}')
                with open(file_path, 'w') as csv_file:
                    writer = csv.writer(csv_file)
                    for num in range(self.file_size):
                        group = next(groups)
                        writer.writerow([group.name, group.email])

        self.mark_groups_as_used()

    def mark_groups_as_used(self):
        groups_ids = self._get_all_groups_ids()
        qs = FbGroup.download_objects.filter(pk__in=groups_ids)
        print(f'\nStart mars as used, {len(groups_ids)} groups')
        qs.mark_as_used()


class FileGroupQuery:
    QSS = {
        'new': FbGroup.download_objects.new(),
        'used': FbGroup.download_objects.used(FileGroupDrawer.USED_COUNT).rested().order_by('-send_last_date'),

        'new_corp': FbGroup.download_objects.new().corp_mails(),
        'new_not_corp': FbGroup.download_objects.new().not_corp_mails().order_by('?'),
        'used_corp': FbGroup.download_objects.used(FileGroupDrawer.USED_COUNT).corp_mails().rested().order_by('-send_last_date'),
        'used_not_corp': FbGroup.download_objects.used(FileGroupDrawer.USED_COUNT).not_corp_mails().rested().order_by('-send_last_date'),
    }

    def __init__(self, qs_type, files_count, file_drawer):
        self.file_drawer = file_drawer
        self.qs_type = qs_type
        self.files_count = files_count
        self._check_type()
        self.qs = self.QSS[self.qs_type][:self.slice]
        self._check_is_qs_full()


    def __repr__(self):
        return f'FileGroupQuery: {self.qs_type} {self.files_count} ({self.slice})'

    def __len__(self):
        return len(self.qs)

    def _check_type(self):
        if self.qs_type not in FileGroupQuery.QSS:
            raise ValueError(f'Incorrect qs type: {self.qs_type}')

    def _check_is_qs_full(self):
        qs_len = len(self.qs)
        if self.slice != qs_len:
            raise ValueError(f'Не коректное количество групп в qs {self.qs_type}. Должно быть {self.slice}, по фатку {qs_len}.')

    @property
    def slice(self):
        return self.files_count * self.file_drawer.file_size


file_drawer = FileGroupDrawer()
print('USED COUNT:',FileGroupDrawer.USED_COUNT)
print('File size', file_drawer.file_size)
res = input('you shore?: ', )
if res.lower() not in ['y', 'yes']:
    raise exit()
file_drawer.create_file_qss(new_data_count=0, used_data_count=10, split_corps=False)
file_drawer.info()
file_drawer.create_files()



#create_file()
