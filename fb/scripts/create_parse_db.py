import sqlite3
import os
from ads.models import FbGroup
from proxies.models import ProxyMobile
from django.template import Template, Context

BD_NAME = 'email_parse_groups.db'


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
VALUES 
{%for group in groups%}
('{{group.pk}}', '{{group.status}}', '','','',''){%if not forloop.last%},{%endif%}
{%endfor%}
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



GROUPS_COUNT = """
SELECT COUNT(*) FROM ads_fbgroup
"""


def add_groups(qs):
    template = Template(INSERT_GROUPS_COM)
    content = {
        'groups': qs,
    }
    context = Context(content)
    command = template.render(context)
    cur.execute(command)
    con.commit()

    qs_to_update = FbGroup.objects.filter(pk__in=[group.pk for group in qs])
    qs_to_update.update(is_in_pars_task=True)
    # for group in qs:
    #     group.is_in_pars_task = True
    #     group.save()



def add_proxy(qs):
    for p in qs:
        command = INSERT_PROXY_COM % (p.pk, p.protocol, p.ip, p.port, p.port, p.login, p.password, p.change_ip_url)
        cur.execute(command)
    con.commit()



if os.path.exists(BD_NAME):
    res = input('Db exist,delete? type Yes/y: ')
    if res.lower() not in ['yes', 'y']:
        print('Incorrect answer')
        exit()
    os.remove(BD_NAME)


con = sqlite3.connect(BD_NAME)
cur = con.cursor()

cur.execute(CREATE_GROUPS_TABLE_COM)
cur.execute(CREATE_PROXY_TABLE_COM)

proxies = ProxyMobile.objects.all()


add_proxy(proxies)

for i in range(7):
    print(f'Bunch #{i}')
    groups = FbGroup.objects.filter(status__in=[
        'not_loaded',
        'error_req',
    ]).exclude(is_in_pars_task=True)[:10000]
    add_groups(groups)

#SHOW
# res = cur.execute(SELECT_ALL_GROUPS)
# for row in res.fetchall():
#     print(row)
res = cur.execute(GROUPS_COUNT)
print(res.fetchall())
