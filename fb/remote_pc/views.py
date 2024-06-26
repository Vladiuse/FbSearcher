from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import DS, Settings, DSDailyStat
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

def index(request):
    content = {

    }
    return render(request, 'remote_pc/index.html')
@login_required
def active(request):
    """Страница со статусами работы"""
    show_site_not_load_block_time =  Settings.objects.get(pk='show_site_not_load_block_time')
    main_page_reload_time = Settings.objects.get(pk='main_page_reload_time')
    dss = DS.objects.filter(use_in_pars=True)
    active_count = len(list(filter( lambda ds: ds.status['text'] == DS.WORK,dss)))
    is_not_word_exists = any(ds.status['text'] == DS.NOT_WORK for ds in dss)
    # active_count = 0
    # is_not_word_exists = False
    # for ds in dss:
    #     if ds.status()['text'] == DS.WORK:
    #         active_count += 1
    #     if ds.status()['text'] == DS.NOT_WORK:
    #         is_not_word_exists = True
    content = {
        'dss': dss,
        'show_site_not_load_block_time': show_site_not_load_block_time,
        'main_page_reload_time': main_page_reload_time,
        'active_count': active_count,
        'is_not_word_exists': is_not_word_exists,
    }
    return render(request, 'remote_pc/active.html', content)

def parse_stat(request):
    content = {
        'last_parse_date': DS.last_parse_date(),
        'daily_stat_total':  DS.daily_total_stat(),
        'dss_today_stat': DS.dss_today_stat(),
        'dss_avg_stat': DS.dss_avg_stat,
        'country_last_date_new_stat': DSDailyStat.country_last_date_new_stat(),
        'total_new_stat': DSDailyStat.total_new_stat(),
    }
    return render(request, 'remote_pc/parse_stat.html', content)
@require_http_methods(['GET'])
def ping_ds(request, ds_name):
    """Ручка для пропинговки дедиками"""
    try:
        ds = DS.objects.get(name=ds_name)
    except DS.DoesNotExist:
        return HttpResponse('Incorrect DS name', status=404)
    ds.ping()
    return HttpResponse('Ping success')

