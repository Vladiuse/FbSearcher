import sqlite3
import os
from ads.models import FbGroup
from django.db.utils import OperationalError

GET_GROUPS_COMM = """
SELECT group_id, name, title, email, followers, status
FROM ads_fbgroup
"""

BD_NAME = 'email_parse_groups.db'

con = sqlite3.connect(BD_NAME)
cur = con.cursor()
groups = cur.execute(GET_GROUPS_COMM)
groups_in_db = 0
emails_count = 0
for_bit_names = 0
for num, group_from_parse in enumerate(groups):
    group_id, name, title, email, followers, status = group_from_parse
    groups_in_db += 1
    if email:
        emails_count += 1
    group = FbGroup.objects.get(pk=group_id)
    group.name = name
    group.title = title
    group.email = email
    group.followers_list = followers
    group.status = status
    group.is_in_pars_task = False
    try:
        group.save()
    except OperationalError as error:
        print(error)
        print(num,group)
        print(group_from_parse)
        group = FbGroup.objects.get(pk=group_id)
        group.is_in_pars_task = False
        group.status = FbGroup.FOURBIT_CHAR_IN_NAME
        group.save()
        for_bit_names += 1

main_percent = int(round(emails_count / groups_in_db,2) * 100)
print(f'Total: {groups_in_db}, with emails: {emails_count}  (main_percent%), 4bit: {for_bit_names}')
