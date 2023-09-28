from django.contrib import admin
from django import forms
from .models import Proxy
from .form import ProxyForm

class ProxyAdmin(admin.ModelAdmin):
    form = ProxyForm
    actions = ['check_proxies']
    list_display = ['pk', 'fbaccount','comment','ip','port', 'url', 'status', 'error_text_short', 'created']
    list_display_links = ['pk', 'ip']
    search_fields = ['comment']
    @admin.action(description='Проверить прокси')
    def check_proxies(self, request, queryset):
        queryset.update(status=Proxy.NOT_CHECKED)
        Proxy.check_proxies(qs=queryset)

    def error_text_short(self, obj):
        if obj.error_text:
            return obj.error_text[:40] + '...'
        return obj.error_text

admin.site.register(Proxy, ProxyAdmin)

