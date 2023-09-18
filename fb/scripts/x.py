from ads.models import FbGroup
from ads.fb_group_page import FbGroupPage

group = FbGroup.objects.filter(status=FbGroup.NEED_LOGIN)
print(len(group))
# for g in group:
#     if not g.email and not g.name:
#         print(g, g.email, g.name)