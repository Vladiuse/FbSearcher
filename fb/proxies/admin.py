from django.contrib import admin

from .models import Proxy


class ProxyAdmin(admin.ModelAdmin):
    actions = ['check_proxies']
    list_display = ['pk', 'data', 'url', 'status', 'error_text_short']

    @admin.action(description='Проверить прокси')
    def check_proxies(self, request, queryset):
        Proxy.check_proxies(qs=queryset)

    def error_text_short(self, obj):
        return obj.error_text[:60] + '...'


admin.site.register(Proxy, ProxyAdmin)
