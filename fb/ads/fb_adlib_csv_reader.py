import csv
from os import zip_path
from zipfile import ZipFile
import io

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
        return zip_path.basename(self.path)

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





class FbLibGeoStatReader:

    def __init__(self, path, file_name=None):
        self.path = path
        self._file_name = file_name
        self.unique_group_ids = list()
        self.total = 0

    @property
    def file_name(self):
        if self._file_name:
            return self._file_name
        return zip_path.basename(self.path)

    def read(self):
        with ZipFile(self.path) as zip:
            data_csv_name = ''
            for file in zip.filelist:
                if file.filename.endswith('_advertisers.csv'):
                    data_csv_name = file.filename
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
        return  spend != '≤100' and int(spend) > 99


    def __len__(self):
        return len(self.unique_group_ids)

    def __getitem__(self, item):
        return self.unique_group_ids[item]


if __name__ == '__main__':
    zip_path = '/home/vlad/PycharmProjects/FbSearcher/_csv_examples/FacebookAdLibraryReport_2023-08-24_SA_last_7_days.zip'
    reader = FbLibGeoStatReader(zip_path)
    reader.read()
    print(reader.total, reader.unique_group_ids)
