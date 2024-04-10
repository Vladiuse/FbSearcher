from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Country, Language, Currency, KeyWord, WorldPart, CountryComment, CountryLanguage


class KeyWordAdmin(admin.ModelAdmin):
    list_display = ['number_in_dict','word','language_id']
    list_filter = ['language_id']
    search_fields = ['word']


class CountryCurrencyInline(admin.TabularInline):
    model = Country.curr.through
    extra = 0


class CountryAdmin(admin.ModelAdmin):
    list_display = ['iso', 'ru_full_name', 'phone', 'phone_code', ]
    list_display_links = ['iso', 'ru_full_name']
    search_fields = ['iso', 'ru_full_name']
    autocomplete_fields = ['language', 'curr']

    inlines = [
        CountryCurrencyInline,
    ]

    list_filter = (
        ('phone', admin.EmptyFieldListFilter),
    )


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['upper_iso', 'name']
    search_fields = ['iso', 'name']

    inlines = [
        CountryCurrencyInline,
    ]

    @admin.display
    def upper_iso(self, obj):
        return obj.iso.upper()


class LanguageAdmin(admin.ModelAdmin):
    list_display = ['iso', 'russian_name']
    search_fields = ['russian_name', 'iso']

class CityAdmin(admin.ModelAdmin):
    list_display = ['country_id', 'name', 'use_in_text_search']
    list_display_links = ['name']
    search_fields = ['name']

class CountryCommentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['country',]
class WorldPartAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']

class CountryLanguageAdmin(admin.ModelAdmin):
    list_display = ['country', 'language', 'keys_deep']
    search_fields = ['country__pk', 'language__iso']
    list_editable = ['keys_deep']

admin.site.register(Country, CountryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Currency,CurrencyAdmin)
admin.site.register(KeyWord, KeyWordAdmin)
admin.site.register(WorldPart, WorldPartAdmin)
admin.site.register(CountryComment,CountryCommentAdmin)
admin.site.register(CountryLanguage, CountryLanguageAdmin)