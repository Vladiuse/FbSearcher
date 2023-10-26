from parsers.fb_ads_lib_parser_new.main  import parse_by_keys
from ads.models import KeyWord

keys = KeyWord.objects.filter(number_in_dict__range=(1000, 2000)).order_by('?')[:40]
# keys = KeyWord.objects.order_by('?')[:40]
parse_by_keys(keys)
