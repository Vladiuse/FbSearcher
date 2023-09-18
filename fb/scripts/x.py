from ads.models import FbGroup
from ads.fb_group_page import FbGroupPage

# for num,group in enumerate(FbGroup.objects.all()):
#     print(num, group)
#     group.get_req_html_data()

for group in FbGroup.objects.all():
    with open(group.req_html_data.path) as file:
        html = file.read()
    page = FbGroupPage(html)
    page()
    res = page.result
    if page.is_login_form:
        print(group, page.group_name, page.group_email)