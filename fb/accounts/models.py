from django.db import models
import http.cookiejar
from django.core.exceptions import ValidationError
import os
from http.cookiejar import LoadError
from proxies.models import Proxy
from parsers import FbMainPage
import requests as req


class FbAccount(models.Model):
    WORK = 'work'
    BAN = 'ban'
    STATUSES = (
        (WORK, 'Рабочий'),
        (BAN, 'Бан')
    )
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUSES, default=WORK)
    cookie_file = models.FileField(upload_to='cookies') #  TODO rename to cookie_file
    created = models.DateField(auto_now_add=True)
    proxy = models.OneToOneField(Proxy, on_delete=models.SET_NULL,blank=True,null=True )
    use_in_work = models.BooleanField(default=True)
    is_cookie_file_valid = models.BooleanField(default=None, null=True)
    is_cookie_auth = models.BooleanField(default=None, null=True)

    def __str__(self):
        return self.name

    def check_cookie_auth(self):
        """Проверить являються ли куки актуальными, залогинен ли аккаунт под ними"""
        if not self.is_cookie_file_valid:
            self.is_cookie_auth = None
        else:
            res = req.get(FbMainPage.URL,
                          cookies=self.get_cookie(),
                          proxies={'https': self.proxy.url},
                          )
            if not res.status_code == 200:
                raise ZeroDivisionError(res.status_code)
            # log
            with open(f'/home/vlad/html/{self.name}.html', 'w') as file:
                file.write(res.text)

            page = FbMainPage(res.text)
            self.is_cookie_auth = page.is_auth
        self.save()

    def check_cookie_file(self):
        """Проверить файл куки на валидность"""
        jar = http.cookiejar.MozillaCookieJar(self.cookie_file.path)
        try:
            jar.load()
            self.is_cookie_file_valid = True
            self.save()
        except LoadError:
            self.is_cookie_file_valid = False
            self.save()
            raise LoadError

    def get_cookie(self):
        """Получить куки из файла"""
        jar = http.cookiejar.MozillaCookieJar(self.cookie_file.path)
        jar.load()
        return jar



    # def save(self, **kwargs):
    #     if not self.pk:
    #         self._check_cookie_file()
    #     super().save(**kwargs)
    #
    # def clean(self):
    #     print('CLEN')
    #     # print(self.cookie, self.cookie.path)
    #     # print(os.path.exists(self.cookie.path))
    #     for i in dir(self.cookie):
    #         print(i)
    #     print(self.cookie.file,self.cookie.read())
    #     return super().clean()
    #
    # def full_clean(self, *args, **kwargs):
    #     # print('FULL CLEN')
    #     # print(os.path.exists(self.cookie.path))
    #     return super().full_clean(*args, **kwargs)
