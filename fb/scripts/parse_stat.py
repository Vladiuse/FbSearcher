from ads.models import FbGroup
from ads.fbgroup_link_parser import get_fbgroup_id_from_url
import os
from datetime import datetime
from time import time

def _k(num):
    if num > 1000:
        num = round(num / 1000,1)
        return str(num) + 'k'
    return str(num)

def get_file_stat(file_path):
    links = set()
    total_count = 0
    if os.path.exists(file_path):
        life_time = time() - os.path.getctime(file_path)
        with open(file_path) as file:
            for line in file:
                group_id = get_fbgroup_id_from_url(line)
                if group_id:
                    links.add(group_id)
                    total_count += 1
                else:
                    pass
        parse_speed_unique = _k(round(len(links)/life_time *3600))
        parse_speed_total = _k(round(total_count/life_time *3600))

        print(f'{os.path.basename(file_path)}, lifetime: {round(life_time)}')
        print(f'Unique: {len(links)} (~{parse_speed_unique})')
        print(f'Total: {total_count} (~{parse_speed_total})')
        print('\n')


fb_parser_file = '/home/vlad/links.txt'
adhear_parser_file = '/home/vlad/links_heart.txt'

print('Current Time: ', datetime.now().strftime('%H:%M:%S'))
for file_path in fb_parser_file, adhear_parser_file:
    get_file_stat(file_path)
