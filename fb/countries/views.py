from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Country, CountryLanguage, Language, KeyWord, CountryComment, WorldPart
from .forms import CountryLanguageForm
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse
from django.views.generic import CreateView
from django.db.models import Prefetch

def index(request):
    countries = Country.objects.filter(use_in_parse=True).order_by('-population')
    world_parts = WorldPart.objects.prefetch_related(Prefetch(
       'country', queryset=countries
    ))

    content = {
        'world_parts': world_parts,
    }
    return render(request, 'countries/index.html', content)

def country(request, pk):
    country = Country.objects.get(pk=pk)
    country_stat = country.stat()
    content = {
        'country': country,
        'country_stat': country_stat,
        'country_new_daily_stat': country.country_new_daily_stat(),
    }
    return render(request, 'countries/country.html', content)


class ShowLibrary(View):

    def post(self, request):
        country = Country.objects.get(pk=request.POST['country'])
        language = Language.objects.get(pk=request.POST['language'])
        number_in_dict = request.POST['number_in_dict']
        keyword = KeyWord.objects.get(language=language, number_in_dict=number_in_dict)
        adslib_url = f'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={country.pk.upper()}&q={keyword.word}&publisher_platforms[0]=facebook&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&start_date[min]=2023-12-17&start_date[max]=&search_type=keyword_unordered&media_type=all'
        return HttpResponseRedirect(adslib_url)


class CountryLanguageUpdateView(UpdateView):

    queryset = CountryLanguage.objects.all()
    template_name = 'countries/test.html'
    fields = ['keys_deep', 'weight']

    def get_success_url(self):
        obj = self.get_object()
        return reverse("countries:country", kwargs={"pk": obj.country_id})


class CountryCommentCreateView(CreateView):
    queryset = CountryComment.objects.all()
    fields = ['text', 'country', 'type']

    def get_success_url(self):
        country = Country.objects.get(pk=self.request.POST['country'])
        return reverse("countries:country", kwargs={"pk":country.pk})

class CountryCommentDeleteView(DeleteView):
    queryset = CountryComment.objects.all()

    def get_success_url(self):
        obj = self.get_object()
        country = Country.objects.get(pk=obj.country)
        return reverse("countries:country", kwargs={"pk":country.pk})




