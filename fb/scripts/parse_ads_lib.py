from parsers.fb_ads_lib_parser_new.main  import parse_by_keys
from ads.models import KeyWord
import configparser


conf_path = 'conf.ini'
config = configparser.ConfigParser()
config.read(conf_path)
start_key = int(config.get('AdsLibParser', 'start_key'))
end_key = int(config.get('AdsLibParser', 'end_key'))
keys_count = int(config.get('AdsLibParser', 'keys_count'))
country = config.get('AdsLibParser', 'country')

keys = KeyWord.objects.filter(number_in_dict__range=(start_key, end_key)).order_by('?')[:keys_count]
parse_by_keys(keys, country)
