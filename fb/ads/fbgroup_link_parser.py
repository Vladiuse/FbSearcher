import re

def get_fbgroup_id_from_url(url:str) -> str:
    url = url.replace('http://', 'https://')
    url = url.replace('://www.','://' )
    if not url.endswith('/'):
        url = url + '/'
    patterns = [
        r'^https://facebook.com/\d{3,30}/$',
        r'^https://facebook.com/.{3,80}/$',
        r'^https://fb.com/page-\d{3,30}/$',
    ]
    for pattern in patterns:
        if re.match(pattern, url):
            url = url[:-1]
            url = url.replace('https://facebook.com/', '')
            url = url.replace('https://fb.com/page-', '')
            return url
    return ''


