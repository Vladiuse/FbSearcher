import csv
from os import path
from zipfile import ZipFile
import io
import sys



csv.field_size_limit(sys.maxsize)

# TODO write reader exception
class FbLibStatCsvReader:

    def __init__(self, path, file_name=None):
        self.path = path
        self._file_name = file_name
        self.unique_group_ids = list()
        self.total = 0

    @property
    def file_name(self):
        if self._file_name:
            return self._file_name
        return path.basename(self.path)

    def read(self):
        unique = set()
        with open(self.path, 'r', encoding='utf-8') as csv_file:
            table = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            for row in table:
                unique.add(row['page_id'])
                self.total += 1
        self.unique_group_ids.extend(unique)
        return self

    def __len__(self):
        return len(self.unique_group_ids)

    def __getitem__(self, item):
        return self.unique_group_ids[item]


class FbLibStatZipReader:
    """Читает zip с отчетом из AdsLib"""
    def __init__(self, path, file_name=None):
        self.path = path
        self._file_name = file_name
        self.unique_group_ids = list()
        self.total = 0

    @property
    def file_name(self):
        if self._file_name:
            return self._file_name
        return path.basename(self.path)

    def read(self):
        with ZipFile(self.path) as zip:
            file_path = zip.filelist[0].filename # TODO if len > 1 if len 0
            with io.TextIOWrapper(zip.open(file_path), encoding='utf-8') as csv_file:
                unique = set()
                table = csv.DictReader(csv_file, delimiter=',', quotechar='"')
                for row in table:
                    unique.add(row['page_id'])
                    self.total += 1
            self.unique_group_ids.extend(unique)
            return self


    def __len__(self):
        return len(self.unique_group_ids)

    def __getitem__(self, item):
        return self.unique_group_ids[item]




class Fb7DaysZipReader:
    """Читает zip с отчетом за 7 дней"""
    def __init__(self, path, file_name=None):
        self.path = path
        self._file_name = file_name
        self.unique_group_ids = list()
        self.total = 0

    @property
    def file_name(self):
        if self._file_name:
            return self._file_name
        return path.basename(self.path)

    def read(self):
        with ZipFile(self.path) as zip:
            data_csv_name = ''
            for file in zip.filelist:
                if file.filename.endswith('_advertisers.csv'):
                    data_csv_name = file.filename
            if not data_csv_name:
                raise TypeError('Нужный файл в архиве не найден')
            with io.TextIOWrapper(zip.open(data_csv_name), encoding='utf-8') as csv_file:
                table = csv.reader(csv_file, delimiter=',', )
                header = next(table)
                unique_pages_ids = set()
                for line in table:
                    self.total += 1
                    page_id, spend = line[0], line[3]
                    if self.is_big_spend(spend):
                        unique_pages_ids.add(page_id)
                self.unique_group_ids.extend(unique_pages_ids)


    def is_big_spend(self, spend):
        return spend != '≤100' and int(spend) > 99


    def __len__(self):
        return len(self.unique_group_ids)

    def __getitem__(self, item):
        return self.unique_group_ids[item]


if __name__ == '__main__':
    pass
    # zip_path = '/home/vlad/PycharmProjects/FbSearcher/_csv_examples/FacebookAdLibraryReport_2023-08-24_SA_last_7_days.zip'
    # reader = Fb7DaysZipReader(zip_path)
    # reader.read()
    # print(reader.total, reader.unique_group_ids)

    fb_ads_lib_zip_path = '/home/vlad/PycharmProjects/FbSearcher/_csv_examples/meta_data/meta-ad-library-19_9_2023_2.zip'
    reader = FbLibStatZipReader(fb_ads_lib_zip_path)
    reader.read()
    print(reader.total)


    print(len(reader))
