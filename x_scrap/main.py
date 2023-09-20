
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

import threading
import time

import requests
from bs4 import BeautifulSoup
import http.cookiejar


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scan Mails")

        self.scanning = False
        self.scanning_task = []

        self.frame1 = tk.Frame(self)
        self.frame1.pack()

        self.total_uid_lbl = ttk.Label(self.frame1, text='Total UID: 0')
        self.total_uid_lbl.grid(column=0, row=0)

        self.result_lbl = ttk.Label(self.frame1, text='Result: 0')
        self.result_lbl.grid(column=1, row=0)

        ttk.Label(self.frame1, text='Thread:').grid(column=0, row=1)

        self.thread_count = ttk.Entry(self.frame1, width=12)
        self.thread_count.grid(column=1, row=1)

        self.thread_count.insert(tk.END, string="50")

        self.btn = ttk.Button(self.frame1, text='Start', width=12, command=self.start_scan)
        self.btn.grid(column=2, row=1)

        self.btn = ttk.Button(self.frame1, text='Stop', width=12, command=self.stop_scan)
        self.btn.grid(column=3, row=1)

        self.frame2 = tk.Frame(self)
        self.frame2.pack(expand=True, fill='both')

        self.text_area = scrolledtext.ScrolledText(self.frame2, wrap=tk.WORD, width=40, height=10)
        self.text_area.pack(expand=True, fill='both')
        self.text_area.insert(tk.INSERT, "")

        self.update_content()
        self.update_total_uid_lbl()
        self.update_result_lbl()

    def update_content(self):
        try:
            with open("result.txt", "r") as file:
                content = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, content)
        except FileNotFoundError:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, "File not found: " + "result.txt")

        self.after(10, self.update_content)

    def update_total_uid_lbl(self):
        try:
            with open("uids.txt", "r") as file:
                count = len(file.readlines())
                self.total_uid_lbl.configure(text="Total UID: " + str(count))
        except FileNotFoundError:
            self.total_uid_lbl.configure(text="Total UID: " + "0")

        self.after(10, self.update_total_uid_lbl)

    def update_result_lbl(self):
        try:
            with open("result.txt", "r") as file:
                count = len(file.readlines())
                self.result_lbl.configure(text="Result: " + str(count))
        except FileNotFoundError:
            self.result_lbl.configure(text="Result: " + "0")

        self.after(10, self.update_result_lbl)

    def get_info_by_uid(self, uid: str):
        self.scanning_task.append(uid)

        def load_netscape_cookies(cookie_file):
            jar = http.cookiejar.MozillaCookieJar(cookie_file)
            jar.load()
            return jar

        def get_user_info_by_uid(uid: int):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5'
            }

            r = requests.get('https://www.facebook.com/profile.php?id={}'.format(uid), headers=headers,
                             cookies=load_netscape_cookies('cookies.txt'))

            soup = BeautifulSoup(r.content, 'html.parser')

            # Get username
            username = None

            username_element = soup.find('h1', class_='x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz')
            if username_element:
                span_element = username_element.find("span", class_="xt0psk2")
                if span_element:
                    span_element.extract()

                username = username_element.get_text().strip()

            # Get mail address
            email = None

            email_icon_element = soup.find('img',
                                           {'src': 'https://static.xx.fbcdn.net/rsrc.php/v3/yE/r/2PIcyqpptfD.png'})
            if email_icon_element:
                email_text_content = email_icon_element.parent.parent.get_text().strip()
                email = email_text_content

            return username, email

        try:
            uname, mail = get_user_info_by_uid(uid=int(uid))

        except Exception as ex:
            print(ex)

        else:
            info_line = str(uid) + '|' + str(uname) + '|' + str(mail)
            with open('result.txt', 'a') as result_f:
                result_f.write(info_line + '\n')

        finally:
            self.scanning_task.remove(uid)

    def scan(self):
        try:
            with open('uids.txt', 'r') as f:
                uids = f.readlines()

            while any(uids):
                if self.scanning is not True:
                    break

                while len(self.scanning_task) > int(self.thread_count.get()):
                    time.sleep(0.1)

                uid = uids.pop().strip()

                t = threading.Thread(target=self.get_info_by_uid(uid=uid))
                t.start()

                with open('uids.txt', 'w') as fw:
                    fw.write(''.join(uids))

        except Exception as ex:
            print(ex)

        finally:
            self.scanning = False

    def start_scan(self):
        if self.scanning is True:
            return

        self.scanning = True
        scan_thread = threading.Thread(target=self.scan, args=[])
        scan_thread.start()

    def stop_scan(self):
        if self.scanning is True:
            self.scanning = False


if __name__ == "__main__":
    app = App()
    app.mainloop()
