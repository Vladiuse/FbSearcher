import os.path

from django.contrib import admin
from .models import FbGroup, FbPagExample, MailService, IgnoredMailGeo, IgnoreGroupWord
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

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
    list_display = ['pk', 'status','name' ,'title','email','email_service', 'followers','url_link', 'req_log_file']
    list_display_links = ['pk']
    list_filter = ['status', FbGroupDataFilter, 'created']
    search_fields = ['pk', 'title', 'name', 'email']
    actions = ['clean_all_data', 'mark_names']

    def url_link(self, obj):
        return mark_safe(f'<a target="_blank" href="{obj.url}">Open group<a/>')

    def req_log_file(self, obj):
        if obj.req_html_data and os.path.exists(obj.req_html_data.path):
            return mark_safe(f'<a target="_blank" href="{obj.req_html_data.url}">{obj.pk}<a/>')
        return '-'

    @admin.action(description='Сбросить данные')
    def clean_all_data(self, request, queryset):
        print('Сбросить данные')
        FbGroup.clean_all_data(queryset)

    @admin.action(description='Пометить группы')
    def mark_names(self, request, qs):
        for group in qs:
            group.mark_name()


class FbPageExampleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type', 'desc', 'name','is_auth']
    list_display_links = ['pk', 'name']

class MaiServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'pattern', 'ignore']

admin.site.register(FbGroup, FbGroupAdmin)
admin.site.register(FbPagExample, FbPageExampleAdmin)
admin.site.register(MailService, MaiServiceAdmin)
admin.site.register(IgnoredMailGeo)
admin.site.register(IgnoreGroupWord)
