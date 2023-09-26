from django.contrib import admin
from .models import FbGroup
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
        if self.value() == self.EMPTY:
            return queryset.filter(name='').filter(email='')
        if self.value() == self.NO_MAIL:
            return queryset.exclude(name='').filter(email='')
        if self.value() == self.FULL:
            return queryset.exclude(name='').exclude(email='')

class FbGroupAdmin(admin.ModelAdmin):
    list_display = ['pk', 'status','name' ,'email', 'url_link']
    list_display_links = ['pk']
    list_filter = ['status', FbGroupDataFilter]

    def url_link(self, obj):
        return mark_safe(f'<a target="_blank" href="{obj.url}">{obj.url}<a/>')


admin.site.register(FbGroup, FbGroupAdmin)
