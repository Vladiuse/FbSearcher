import csv

class FbLibStatCsvReader:

    def __init__(self, path):
        self.path = path
        self.group_ids = set()
        self.total = 0

    def __call__(self):
        with open(self.path, 'r', encoding='utf-8') as csv_file:
            table = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            for row in table:
                self.group_ids.add(row['page_id'])
                self.total += 1
        return self

    def __len__(self):
        return len(self.group_ids)