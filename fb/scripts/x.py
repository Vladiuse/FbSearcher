from ads.models import FbGroup
from accounts.models import FbAccount
from parsers import FbGroupPage
from proxies.models import Proxy
from time import sleep
import requests as req

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

group = FbGroup.objects.get(pk='zorgerspetcare')
# fb_account = FbAccount.objects.get(pk=2)
# proxy = Proxy.objects.get(pk=10)
fb_account = FbAccount.objects.get(pk=4)
proxy = Proxy.objects.get(pk=9)
res = req.get('https://facebook.com/169566796514206/',
              headers=headers,
              cookies=fb_account.get_cookie(),
              proxies={'https':proxy.url}
              )
print(res.status_code)
with open('/home/vlad/html/fb_group.html', 'w') as file:
    file.write(res.text)



# <FbGroup> https://facebook.com/YackConstruction/
# <FbGroup> https://facebook.com/MitchellCommunityCollege/
# <FbGroup> https://facebook.com/orlandoseamlessgutter/
# <FbGroup> https://facebook.com/constructionleadingedge/
# <FbGroup> https://facebook.com/KalamazooValleyCommunityCollege/
#
# <FbGroup> https://facebook.com/105344305919597/
# <FbGroup> https://facebook.com/398233886974905/
# <FbGroup> https://facebook.com/829786213807107/
# <FbGroup> https://facebook.com/195261533834361/
# <FbGroup> https://facebook.com/104256298922171/


