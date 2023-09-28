from django.contrib import admin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib import messages
from http.cookiejar import LoadError
from .models import FbAccount
from .forms import FbAccountForm



class FbAccountAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'proxy','status', 'created', 'use_in_work', 'cookie_file', 'is_cookie_file_valid', 'is_cookie_auth', 'check_text']
    list_display_links = ['pk', 'name']
    actions = ['check_cookies', 'check_cookies_auth', ]
    form = FbAccountForm
    autocomplete_fields = ['proxy']

    @admin.action(description='Проверить файлы куки')
    def check_cookies(self, request, qs):
        incorrect_accounts = []
        for account in qs:
            try:
                account.check_cookie_file()
            except LoadError as error:
                incorrect_accounts.append(account)
        if incorrect_accounts:
            msg = 'Некоректные куки у: ' + ' ,'.join(account.name for account in incorrect_accounts)
            messages.add_message(request, messages.ERROR, msg)

    @admin.action(description='Проверить авторизацию куки')
    def check_cookies_auth(self, request, qs):
        for account in qs:
            account.check_cookie_auth()


admin.site.register(FbAccount, FbAccountAdmin)