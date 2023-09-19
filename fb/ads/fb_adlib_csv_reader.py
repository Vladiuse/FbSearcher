import csv
from os import path


class FbLibStatCsvReader:

    def __init__(self, path):
        self.path = path
        self.unique_group_ids = list()
        self.total = 0

    @property
    def file_name(self):
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
