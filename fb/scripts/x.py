from ads.models import FbGroup
from accounts.models import FbAccount
from parsers import FbGroupPage
from time import sleep

# fb_account = FbAccount.objects.get(name='vlad')
# for group in FbGroup.not_loaded_objects.all()[:5]:
#     sleep(5)
#     print(group)
#     group.update_group_info(cookies_path=fb_account.cookie.path)



# group = FbGroup.objects.get(pk='springhillmemorial')
# with open(group.req_html_data.path) as file:
#     text = file.read()
# page = FbGroupPage(html=text)
# page()
# print(page.result)
done = [
    'YackConstruction',
    'MitchellCommunityCollege',
    'orlandoseamlessgutter',
    'constructionleadingedge',
    'KalamazooValleyCommunityCollege',
]
for group in FbGroup.objects.filter(pk__in=done):
    print(group, group.status, group.name, group.email)


# <FbGroup> https://facebook.com/YackConstruction/
# <FbGroup> https://facebook.com/MitchellCommunityCollege/
# <FbGroup> https://facebook.com/orlandoseamlessgutter/
# <FbGroup> https://facebook.com/constructionleadingedge/
# <FbGroup> https://facebook.com/KalamazooValleyCommunityCollege/

