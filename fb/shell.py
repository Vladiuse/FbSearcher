from django.db import connection
from django.db import reset_queries


OLD_Q = list()


def format_sql_query(string):
    return string.replace('WHERE', ' '*4+'\nWHERE')

def show_querys(show,reset=True, time=False):
    global OLD_Q
    # qs = connection.queries
    qs = show
    total_time = 0
    print('\n')
    for i, q in enumerate(qs):
        show_time = ''
        if time:
            total_time+= float(q['time'])
            show_time = f"Time: {q['time']}\n\t"
        query = format_sql_query(q['sql'])
        print(f'[{i}]', show_time, query, )

    print(f'\n-- {len(qs)} queries {round(total_time,2)}--')

    if reset:
        OLD_Q += qs
        reset_queries()


class SHowQ:

    def __init__(self, show, time=False):
        self.show = show
        self.time=time

    def __repr__(self):
        if isinstance(self.show, list):
            show_querys(self.show, time=self.time)
        else:
            show_querys(self.show.queries, time=self.time)
        return ''


S = SHowQ(connection)
SO = SHowQ(OLD_Q)
ST = SHowQ(connection, time=True)

#sad