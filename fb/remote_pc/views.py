from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import DS, Settings
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
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
    return render(request, 'remote_pc/index.html', content)

@require_http_methods(['GET'])
def ping_ds(request, ds_name):
    """Ручка для пропинговки дедиками"""
    try:
        ds = DS.objects.get(name=ds_name)
    except DS.DoesNotExist:
        return HttpResponse('Incorrect DS name', status=404)
    ds.ping()
    return HttpResponse('Ping success')

