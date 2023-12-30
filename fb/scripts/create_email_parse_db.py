import sqlite3
import os
from ads.models import FbGroup



BD_NAME = 'email_parse_groups.db'
if os.path.exists(BD_NAME):
    os.remove(BD_NAME)


con = sqlite3.connect(BD_NAME)
cur = con.cursor()


CREATE_GROUPS_TABLE_COM = """
CREATE TABLE fbgroup(
group_id TEXT PRIMARY KEY,
name TEXT,
title TEXT,
email TEXT,
followers TEXT,
status TEXT)
"""

INSERT_GROUPS_COM = """
INSERT INTO fbgroup
(group_id)
VALUES ('%s')
"""

SELECT_ALL_COMM = """
SELECT * FROM fbgroup
"""

groups = FbGroup.objects.all()[:10]

cur.execute(CREATE_GROUPS_TABLE_COM)
for group in groups:
    command = INSERT_GROUPS_COM % group.pk
    print(command)
    cur.execute(command)

con.commit()

res = cur.execute(SELECT_ALL_COMM)
for row in res.fetchall():
    print(row)



