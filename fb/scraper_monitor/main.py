import threading
from tkinter import *
from tkinter import ttk
from datetime import datetime
from time import time
import random as r
from time import sleep
from threading import Thread
from ads.models import FbGroup
from proxies.models import ProxyMobile
from parsers import FbGroupPageNoAuth
import requests as req
from .devine_array import devine_array
from .fake_objects import ResponseFake, RequestFake, ProxyFake
from proxies.models import ProxyChangeIpUrlNotWork, ProxyChangeIpTimeOutError
from requests.exceptions import RequestException

groups = FbGroup.objects.exclude(status='collected')[:20000]
proxy_4 = ProxyMobile.objects.get(pk=4)
proxy_3 = ProxyMobile.objects.get(pk=3)

ERROR_REQ_COLOR = '#dc0000'
NO_DATA_COLOR = '#F1C830'
NO_MAIL_COLOR = '#BFF130'
LOGIN_FORM = '#3082F1'
FULL_DATA = '#39F130'

REQ_TEST = RequestFake()


class ProxyStream:
    """
    Класс для потока прокси
    """
    REQ_BAR_MAX_LEN = 35
    REQ_TIMEOUT = 6

    def __init__(self, stream_num, proxy_bar, proxy, groups):
        self.stream_num = stream_num
        self.proxy_bar = proxy_bar
        self.proxy = proxy
        self.reqs = []
        self.groups = groups
        self.is_complete = False
        self.is_pause = False

        # counters
        self.success_reqs_count = 0
        self.emails_count = 0
        self.error_reqs_count = 0
        self.reqs_count = 0

        # stream frame
        self.stream_frame = ttk.Frame(self.proxy_bar.frame, borderwidth=1, relief='solid', padding=[5, 5], )
        self.stream_frame.pack(padx=5, pady=2, expand=True, fill=X)

        # line 2
        self.progress_frame = ttk.Frame(self.stream_frame, )
        self.progress_frame.pack(padx=5, expand=True, fill=X)
        self.stream_name_label = ttk.Label(self.progress_frame, text=f'Thread #{self.stream_num}')
        self.stream_name_label.grid(row=0, column=0)
        self.stream_progress_label = ttk.Label(self.progress_frame, text=f'({0}/{len(self.groups)})')
        self.stream_progress_label.grid(row=0, column=1, padx=5)
        self.progress_bar = ttk.Progressbar(self.progress_frame, maximum=len(self.groups), value=0, length=500, )
        self.progress_bar.grid(row=0, column=2)
        self.pause_stream_btn = ttk.Button(self.progress_frame, text=f'Pause', command=self.click_pause)
        self.pause_stream_btn.grid(row=0, column=3, padx=5, )

        self.status_frame = ttk.Frame(self.stream_frame, )
        self.status_frame.pack(padx=5, expand=True, fill=X)
        self.success_reqs_label = ttk.Label(self.status_frame, text=f'Success: {0}')
        self.success_reqs_label.pack(side=LEFT)
        self.mails_count_label = ttk.Label(self.status_frame, text=f'Mails: {0}')
        self.mails_count_label.pack(side=LEFT, padx=5)
        self.errors_count_label = ttk.Label(self.status_frame, text=f'Errors: {0}')
        self.errors_count_label.pack(side=LEFT, padx=5)
        self.reqs_canvas = Canvas(self.status_frame, bg='grey', width=460, height=20)
        self.reqs_canvas.pack(side=LEFT, padx=5)

    def run(self):
        """Главный цикл потока, перебирает ссылки и парсит"""
        for num, group in enumerate(self.groups):
            req_result = group.update_from_url(proxy=self.proxy, timeout=self.REQ_TIMEOUT)
            # req_result = REQ_TEST.get('')  # FAKE
            self.reqs.append(req_result)
            self.update_req_counters(req_result)
            if self.is_pause:
                self._wait_pause()
        self.set_complete()

    def click_pause(self):
        """ Событие при клике на кнопку "пауза" прокси"""
        if self.is_pause:
            self.activate()
        else:
            self.pause()

    def activate(self):
        """Сделать поток активным - продолжит парсить"""
        self.is_pause = False
        self.pause_stream_btn['text'] = 'Pause'

    def pause(self):
        """Поставить поток на паузу"""
        self.is_pause = True
        self.pause_stream_btn['text'] = 'Active'

    def _clean_old_req_data(self):
        """Отчистить старые данные по запросам (они не будут отобрадатсья в баре)"""
        pass
        # TODO

    def _wait_pause(self):
        """Ожидание окончания паузы"""
        while self.is_pause:
            sleep(1)

    def set_complete(self):
        """Пометить поток как закончивший парсинг"""
        self.is_complete = True
        self.stream_name_label['background'] = '#96DB33'
        self.proxy_bar.set_complete()

    def update_req_counters(self, req_result: dict):
        """обновить счетчики потока класса по результату потока"""
        self.reqs_count += 1
        if req_result['status']:
            self.success_reqs_count += 1
            if 'email' in req_result['result']:
                self.emails_count += 1
        else:
            self.error_reqs_count += 1
        self.proxy_bar.up_req_count()
        self._update_counters_tkk()
        self._draw_canvas_reqs()

    def _draw_canvas_reqs(self):
        """Отрисовать статусы запросов цветами"""
        self.reqs_canvas.delete('all')
        padding = 3
        height = 16
        width = 10
        top = 2
        if len(self.reqs) < self.REQ_BAR_MAX_LEN:
            line = self.reqs
        else:
            line = self.reqs[-self.REQ_BAR_MAX_LEN:]
        for i, req_result in enumerate(line):
            if req_result['status']:
                if not req_result['result']:
                    fill = NO_DATA_COLOR
                elif 'email' not in req_result['result']:
                    fill = NO_MAIL_COLOR
                else:
                    fill = FULL_DATA
            else:
                fill = ERROR_REQ_COLOR
            self.reqs_canvas.create_rectangle(
                i * (width + padding), top, i * (width + padding) + width, padding + height,
                outline=fill, fill=fill)

    def _update_counters_tkk(self):
        """Обсновить счетчики запросов в графике"""
        self.stream_progress_label['text'] = f'({self.reqs_count}/{len(self.groups)})'
        self.progress_bar['value'] = self.reqs_count
        self.success_reqs_label['text'] = f'Success: {self.success_reqs_count}'
        self.mails_count_label['text'] = f'Mails: {self.emails_count}'
        self.errors_count_label['text'] = f'Errors: {self.error_reqs_count}'


class ProxyBar:
    """
    Класс прокси
    """
    STREAM_COUNT = 5

    # auto ip change
    REQ_COUNT_CHANGE_IP = 2 * 1000
    WAIT_AFTER_ERROR_IP_CHANGE = 20
    AUTO_CHANGE_IP = True
    MAX_TRY_IP_CHANGE_ERROR = 5  # not change

    def __init__(self, proxy_num, proxy, groups):
        self.proxy = proxy
        self.groups = groups
        self.total_reqs_count = 0
        self.streams = []
        self._is_paused = False
        self.ip_change_count = 0
        self.cur_ip_req_count = 0
        self._change_ip_error_count = 0

        # ttk
        self.frame = ttk.Frame(borderwidth=1, relief='solid', padding=[5, 10])
        self.frame.pack(padx=5, pady=5, expand=True, anchor='nw', fill=X)
        self.proxy_name_label = ttk.Label(self.frame, text=f'Proxy #{proxy_num}')
        self.proxy_name_label.pack()

        # proxy info frame
        self.proxy_info_frame = ttk.Frame(self.frame)
        self.proxy_info_frame.pack()
        self.proxy_ip_label = ttk.Label(self.proxy_info_frame, text=f'Ip: {self.proxy.ip}:{self.proxy.port}')
        self.proxy_ip_label.pack(side=LEFT, padx=5)
        self.proxy_total_reqs_label = ttk.Label(self.proxy_info_frame, text=f'Total reqs: {self.total_reqs_count}')
        self.proxy_total_reqs_label.pack(side=LEFT, padx=5)
        self.proxy_arg_req_time_label = ttk.Label(self.proxy_info_frame, text='Avg Req: 0')
        self.proxy_arg_req_time_label.pack(side=LEFT, padx=5)
        self.proxy_change_ip_count_label = ttk.Label(self.proxy_info_frame, text=f'Change ip: {self.ip_change_count}')
        self.proxy_change_ip_count_label.pack(side=LEFT, padx=5)
        # proxy actions buttons
        self.proxy_status_label = ttk.Label(self.frame, text=f'Status: work')
        self.proxy_status_label.pack()

        # Actions buttons frame
        self.btn_actions_frame = ttk.Frame(self.frame)
        self.btn_actions_frame.pack()
        self.pause_stream_btn = ttk.Button(self.btn_actions_frame, text=f'Pause proxy',
                                           command=self.pause_streams_btn_click)
        self.pause_stream_btn.pack(side=LEFT, padx=5)
        self.change_ip_btn = ttk.Button(self.btn_actions_frame, text=f'Change Ip', command=self.change_ip_bnt_click)
        self.change_ip_btn.pack(side=LEFT, padx=5)

        group_parts = devine_array(self.groups, ProxyBar.STREAM_COUNT)
        for stream_num in range(ProxyBar.STREAM_COUNT):
            groups_to_stream = group_parts[stream_num]
            proxy_stream = ProxyStream(stream_num + 1, self, self.proxy, groups_to_stream)
            self.streams.append(proxy_stream)

    def change_ip_bnt_click(self):
        self.pause_stream_btn['state'] = ["disabled"]
        self.proxy_status_label['text'] = 'Status: wait stream pause'
        self.pause_all_streams()
        sleep(ProxyStream.REQ_TIMEOUT)  # wait streams continue requests
        thread = Thread(target=self.change_proxy_ip)
        thread.start()

    def change_proxy_ip(self):
        """Сменить айпи прокси"""
        self.proxy_status_label['text'] = 'Status: change ip'
        try:
            new_ip = self.proxy.change_ip()
        except (ProxyChangeIpUrlNotWork, ProxyChangeIpTimeOutError, RequestException) as error:
            self._change_ip_error_count += 1
            self.proxy_status_label['text'] = f'Status: Error({type(error).__name__})'
            self.proxy_ip_label['text'] = f'Ip: no ip'
            self.proxy_status_label['background'] = 'red'
            self.change_ip_btn['text'] = 'Change Ip Again'
            # if auto
            if self._change_ip_error_count >= ProxyBar.MAX_TRY_IP_CHANGE_ERROR:
                self.proxy_status_label['text'] = f'Status: Error(Max try to change ip)'
                return
            if ProxyBar.AUTO_CHANGE_IP:
                sleep(ProxyBar.WAIT_AFTER_ERROR_IP_CHANGE)
                self.change_proxy_ip()
        else:
            self.proxy_status_label['text'] = f'Status: work'
            self.proxy_ip_label['text'] = f'Ip: {new_ip}'
            self.proxy_status_label['background'] = ''
            sleep(1)
            self.activate_all_streams()
            self.ip_change_count += 1
            self._change_ip_error_count = 0
            self._update_ip_change_counter()
        finally:
            self.pause_stream_btn['state'] = []

    def pause_streams_btn_click(self):
        """Действие при клике на кнопку Паузы прокси"""
        if self._is_paused:
            self.activate_all_streams()
        else:
            self.pause_all_streams()

    def pause_all_streams(self):
        """Поставить на паузу все потоки"""
        self.pause_stream_btn['text'] = 'Activate'
        self._is_paused = True
        [stream.pause() for stream in self.streams]

    def activate_all_streams(self):
        self.pause_stream_btn['text'] = 'Pause'
        self._is_paused = False
        [stream.activate() for stream in self.streams]

    def start_parse(self):
        """Начать парсинг в потоках"""
        threads = []
        for proxy_stream in self.streams:
            thread = Thread(target=proxy_stream.run, daemon=True)
            threads.append(thread)
            thread.start()
        self.set_complete()

    def set_complete(self):
        """Проверитб все ли потоки закончили работу"""
        if all(stream.is_complete for stream in self.streams):
            self.proxy_ip_label['background'] = '#96DB33'

    def _get_streams_avg_req_time(self):
        avg_streams = []
        for stream in self.streams:
            if stream.reqs:
                avg = sum(req_data['spend_time'] for req_data in stream.reqs) / len(stream.reqs)
                avg_streams.append(avg)
        return sum(avg_streams) / len(avg_streams)

    def _update_avg_req_time(self): # TODO update not on all requests
        avg = self._get_streams_avg_req_time()
        self.proxy_arg_req_time_label['text'] = f'Avg Req: {round(avg, 1)}'

    def _auto_change_ip(self):
        if self.cur_ip_req_count > ProxyBar.REQ_COUNT_CHANGE_IP:
            self.cur_ip_req_count = 0
            self.change_ip_bnt_click()

    def up_req_count(self):
        """поднять счетчики запросов прокси"""
        self.total_reqs_count += 1
        self.cur_ip_req_count += 1
        self._update_counters()
        self._update_avg_req_time()
        self._auto_change_ip()

    def _update_ip_change_counter(self):
        self.proxy_change_ip_count_label['text'] = f'Change ip: {self.ip_change_count}'

    def _update_counters(self):
        """Отрисовать новые значения счетчиков прокси"""
        self.proxy_total_reqs_label['text'] = f'Total reqs: {self.total_reqs_count}'


def start_parse():
    start_btn['state'] = ["disabled"]
    start_btn['text'] = 'Processed'
    for proxy in proxies_to_run:
        proxy.start_parse()


proxies_to_run = []
# proxies = [proxy, proxy]
proxies = [proxy_3, proxy_4]
# proxies = [ProxyFake(),ProxyFake()]  # FAKE
group_parts = devine_array(list(groups), len(proxies))

# MAIN
root = Tk()
root.geometry('800x1000')
groups_count_label = ttk.Label(text=f'groups to parse: {len(groups)}')
groups_count_label.pack()
start_btn = ttk.Button(text='Start', command=start_parse)
start_btn.pack(pady=10)
legend_frame = ttk.Frame()
legend_frame.pack()
legend_data = [
    ('Ошибка запроса', ERROR_REQ_COLOR),
    ('Нет даты', NO_DATA_COLOR),
    ('Форма входа', LOGIN_FORM),
    ('Нет почты', NO_MAIL_COLOR),
    ('Есть почта', FULL_DATA),
]
for text, color in legend_data:
    label = ttk.Label(legend_frame, text=text, background=color)
    label.pack(side=LEFT, padx=3)

for proxy_num, proxy in enumerate(proxies):
    proxies_to_run.append(ProxyBar(proxy_num + 1, proxy, group_parts[proxy_num]))

root.mainloop()
