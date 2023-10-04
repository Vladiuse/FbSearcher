import threading
from tkinter import *
from tkinter import ttk
from datetime import datetime
from time import time
import random as r
from time import sleep
from threading import Thread




class Response:

    def __init__(self, status_code, text=None):
        self.status_code = status_code
        self.text = text


class Request:

    def get(self, url):
        choices = [
            Response(200, {'name': 'XXX', 'email': 'some@gmail.com'}),
            Response(200, {'name': 'XXX', }),
            Response(300),
        ]
        sleep(r.uniform(0.5, 1.5))
        return r.choice(choices)


def draw_proxy(num):
    frame = ttk.Frame(borderwidth=1, relief='solid', padding=[5, 10])
    frame.pack(padx=5, pady=5, expand=True, anchor='nw', fill=X)
    proxy_name = ttk.Label(frame, text=f'Proxy #{num}')
    proxy_name.pack()
    proxy_ip = ttk.Label(frame, text=f'Ip: 178.120.66.252')
    proxy_ip.pack()
    streams_frame = ttk.Frame(frame, borderwidth=1, relief='solid', padding=[5, 10], )
    streams_frame.pack(padx=5, pady=5, expand=True, fill=X)
    for r in range(0, 6, 2):
        for stream_num in range(1, 4):
            stream_name = ttk.Label(streams_frame, text=f'Thread #{stream_num}')
            stream_name.grid(row=r, column=0)
            progress_bar = ttk.Progressbar(streams_frame, maximum=100, value=10, length=500, )
            progress_bar.grid(row=r, column=1)


class ProxyStream:

    REQ_BAR_MAX_LEN = 35

    def __init__(self, proxy):
        self.proxy = proxy
        self.reqs = [r.randint(0,1) for _ in range(r.randint(0,100))]
        self.progress_frame = ttk.Frame(self.proxy.frame, borderwidth=1, relief='solid', padding=[5, 10], )
        self.progress_frame.pack(padx=5, pady=5, expand=True, fill=X)
        self.stream_name_label = ttk.Label(self.progress_frame, text=f'Thread #{1}')
        self.stream_name_label.grid(row=0, column=0)
        self.stream_progress_label = ttk.Label(self.progress_frame, text=f'({10}/{120})')
        self.stream_progress_label.grid(row=0, column=1, padx=5)
        self.progress_bar = ttk.Progressbar(self.progress_frame, maximum=100, value=10, length=500, )
        self.progress_bar.grid(row=0, column=2)
        self.kill_stream_btn = ttk.Button(self.progress_frame, text=f'Kill #{1}', )
        self.kill_stream_btn.grid(row=0, column=3, padx=5, )

        self.status_frame = ttk.Frame(self.proxy.frame, borderwidth=1, relief='solid', padding=[5, 10], )
        self.status_frame.pack(padx=5, pady=5, expand=True, fill=X)
        self.success_reqs_label = ttk.Label(self.status_frame, text='Success: 30')
        self.success_reqs_label.pack(side=LEFT, padx=5)
        self.mails_count_label = ttk.Label(self.status_frame, text='Mails: 15')
        self.mails_count_label.pack(side=LEFT, padx=5)
        self.errors_count_label = ttk.Label(self.status_frame, text='Errors: 3')
        self.errors_count_label.pack(side=LEFT, padx=5)
        self.reqs_canvas = Canvas(self.status_frame,bg='grey',width=460, height=20)
        self.reqs_canvas.pack(side=LEFT, padx=5)
        padding = 3
        height =16
        width = 10
        if len(self.reqs) < self.REQ_BAR_MAX_LEN:
            line = self.reqs
        else:
            line = self.reqs[-self.REQ_BAR_MAX_LEN:]
        print(len(self.reqs), len(line))
        for i,req in enumerate(line):
            top = 2
            if req:
                fill = '#A8D863'
            else:
                fill = '#D87763'
            self.reqs_canvas.create_rectangle(
                i*(width+padding), top, i*(width+padding) + width, padding+ height,
                outline=fill,fill=fill)




class ProxyBar:

    def __init__(self, num):
        self.frame = ttk.Frame(borderwidth=1, relief='solid', padding=[5, 10])
        self.frame.pack(padx=5, pady=5, expand=True, anchor='nw', fill=X)
        self.proxy_name_label = ttk.Label(self.frame, text=f'Proxy #{num}')
        self.proxy_name_label.pack()

        self.proxy_info_frame = ttk.Frame(self.frame)
        self.proxy_info_frame.pack()
        self.proxy_ip_label = ttk.Label(self.proxy_info_frame, text=f'Ip: 178.120.66.252')
        self.proxy_ip_label.pack(side=LEFT, padx=5)
        self.proxy_total_reqs_label = ttk.Label(self.proxy_info_frame, text=f'Total reqs: 10')
        self.proxy_total_reqs_label.pack(side=LEFT, padx=5)

        self.kill_stream_btn = ttk.Button(self.frame, text=f'Kill proxy', )
        self.kill_stream_btn.pack()
        self.streams = [
            ProxyStream(self),
            ProxyStream(self),
            ProxyStream(self),
        ]


root = Tk()
root.geometry('800x600')
for i in range(1, 3):
    ProxyBar(i)

root.mainloop()
#
# class Stream:
#
#     def __init__(self, stream_name):
#         self.value = 0
#         self.progres_label = ttk.Label(text=stream_name)
#         self.progres_bar = ttk.Progressbar(maximum=100, value=self.value, length=500)
#         self.progres_label.pack(pady=10)
#         self.progres_bar.pack()
#
#     def start(self):
#         print('22222')
#         sleep(1)
#         while self.value <= 100:
#             self.value += r.randint(1,8)
#             sleep(0.3)
#             self.progres_bar['value'] = self.value
#         else:
#             self.progres_label['foreground'] = '#B71C1C'
#             self.progres_label['background'] = '#FFCDD2'
#             self.progres_label['text'] = self.progres_label['text'] + ' Complete'
#
# # def draw_bar(stream_name):
# #     s = Stream(stream_name)
# #     s.start()
#
# def main():
#     bars = [Stream(f'Stream #{i}') for i in range(5)]
#     for bar in bars:
#         thread = Thread(target=bar.start)
#         thread.start()
#     print('11111')
#     sleep(10)
#     for t in threading.enumerate():
#         print(t, t.name)
#     # sleep(1)
#     # print('SLEEP 10')
#     # for t in threading.enumerate():
#     #     print(t, t.name)
#
#
# start_btn = ttk.Button(text='start', command=main)
# start_btn.pack()
# root.mainloop()
