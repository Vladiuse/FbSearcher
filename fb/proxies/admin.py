from django.contrib import admin

from .models import Proxy


class ProxyAdmin(admin.ModelAdmin):
    actions = ['check_proxies']
    list_display = ['pk', 'data', 'url', 'status', 'error_text']

    @admin.action(description='Проверить прокси')
    def check_proxies(self, request, queryset):
        for proxy in queryset:
            proxy.check_proxy()


admin.site.register(Proxy, ProxyAdmin)
