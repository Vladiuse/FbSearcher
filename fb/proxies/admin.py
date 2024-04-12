from django.contrib import admin
from django import forms
from .models import Proxy, ProxyAuth, ProxyMobile
from .form import ProxyForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _



class ProxyAdmin(admin.ModelAdmin):
    actions = ['check_proxies', 'change_proxies_ip']
    list_display = ['pk', 'comment','ip','port', 'url', 'status', 'change_ip_url_link', 'error_type', 'created', 'proxy_ip',]
    list_display_links = ['pk', 'ip']
    search_fields = ['comment']
    form = ProxyForm

    def change_ip_url_link(self, obj):
        return mark_safe(f'<a target="_blank" href="{obj.change_ip_url}">Change IP (p{obj.pk})<a/>')

    @admin.action(description='Проверить прокси')
    def check_proxies(self, request, queryset):
        queryset.update(status=Proxy.NOT_CHECKED)
        Proxy.check_proxies(qs=queryset)

    @admin.action(description='Сменить IP')
    def change_proxies_ip(self, request, queryset):
        for proxy in queryset:
            proxy.change_ip()

    def error_text_short(self, obj):
        if obj.error_text:
            return obj.error_text[:40] + '...'
        return obj.error_text

# admin.site.register(Proxy, ProxyAdmin)
# admin.site.register(ProxyAuth, ProxyAdmin)
admin.site.register(ProxyMobile, ProxyAdmin)