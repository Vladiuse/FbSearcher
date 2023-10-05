import os.path

from django.contrib import admin
from .models import FbGroup, FbPagExample, MailService
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

class FbGroupDataFilter(admin.SimpleListFilter):
    title = _('Полнота данных')
    parameter_name = "decade"

    EMPTY = 'empty'
    NO_MAIL = 'no_mail'
    FULL = 'full'

    def lookups(self, request, model_admin):
        return [
            (self.EMPTY, 'Пустой'),
            (self.NO_MAIL, 'Без почты'),
            (self.FULL, 'Полный'),
        ]

    def queryset(self, request, queryset):
        queryset = queryset.filter(status=FbGroup.COLLECTED)
        if self.value() == self.EMPTY:
            return queryset.filter(name='').filter(email='')
        if self.value() == self.NO_MAIL:
            return queryset.exclude(name='').filter(email='')
        if self.value() == self.FULL:
            return queryset.exclude(name='').exclude(email='')

class FbGroupAdmin(admin.ModelAdmin):
    list_display = ['pk', 'status','name' ,'title','email', 'url_link', 'req_log_file']
    list_display_links = ['pk']
    list_filter = ['status', FbGroupDataFilter]
    search_fields = ['pk', 'title', 'name', 'email']

    def url_link(self, obj):
        return mark_safe(f'<a target="_blank" href="{obj.url}">Open group<a/>')

    def req_log_file(self, obj):
        if obj.req_html_data and os.path.exists(obj.req_html_data.path):
            return mark_safe(f'<a target="_blank" href="{obj.req_html_data.url}">{obj.pk}<a/>')
        return '-'
class FbPageExampleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type', 'desc', 'name','is_auth']
    list_display_links = ['pk', 'name']

admin.site.register(FbGroup, FbGroupAdmin)
admin.site.register(FbPagExample, FbPageExampleAdmin)
admin.site.register(MailService)
