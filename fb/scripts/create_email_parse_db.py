import sqlite3
import os
from ads.models import FbGroup
from proxies.models import ProxyMobile

BD_NAME = 'email_parse_groups.db'
if os.path.exists(BD_NAME):
    input('Delete bd?')
    os.remove(BD_NAME)

con = sqlite3.connect(BD_NAME)
cur = con.cursor()

CREATE_GROUPS_TABLE_COM = """
CREATE TABLE ads_fbgroup(
group_id TEXT PRIMARY KEY,
name TEXT,
title TEXT,
email TEXT,
followers TEXT,
status TEXT)
"""

CREATE_PROXY_TABLE_COM = """
CREATE TABLE proxies_proxymobile(
id INTEGER PRIMARY KEY,
protocol TEXT,
ip TEXT,
port TEXT,
login TEXT,
password TEXT,
change_ip_url TEXT
)
"""

INSERT_GROUPS_COM = """
INSERT INTO ads_fbgroup
(group_id, status, name, title, email, followers)
VALUES ('%s', '%s', '','','','')
"""

INSERT_PROXY_COM = """
INSERT INTO proxies_proxymobile
(id,protocol,ip,port,port,login,password,change_ip_url)
VALUES
('%s','%s','%s','%s','%s','%s','%s','%s')
"""

SELECT_ALL_GROUPS = """
SELECT * FROM ads_fbgroup
"""

SELECT_ALL_PROXY = """
SELECT * FROM proxies_proxymobile
"""

cur.execute(CREATE_GROUPS_TABLE_COM)
cur.execute(CREATE_PROXY_TABLE_COM)


def add_groups(qs):
    for group in qs:
        command = INSERT_GROUPS_COM % (group.pk, group.status)
        cur.execute(command)
    con.commit()
    for group in qs:
        group.is_in_pars_task = True
        group.save()



def add_proxy(qs):
    for p in qs:
        command = INSERT_PROXY_COM % (p.pk, p.protocol, p.ip, p.port, p.port, p.login, p.password, p.change_ip_url)
        cur.execute(command)
    con.commit()


groups = FbGroup.objects.filter(status__in=[
    'not_loaded',
    'error_req',
])[:100000]
proxies = ProxyMobile.objects.all()

add_groups(groups)
add_proxy(proxies)

# SHOW
# res = cur.execute(SELECT_ALL_GROUPS)
# for row in res.fetchall():
#     print(row)
