from django.db import models
import http.cookiejar
from django.core.exceptions import ValidationError
import os
from http.cookiejar import LoadError


class FbAccount(models.Model):
    WORK = 'work'
    BAN = 'ban'
    STATUSES = (
        (WORK, 'Рабочий'),
        (BAN, 'Бан')
    )
    name = models.CharField(max_length=50)
    cookie = models.FileField(upload_to='cookies') #  TODO rename to cookie_file
    status = models.CharField(max_length=50, choices=STATUSES, default=WORK)
    created = models.DateField(auto_now_add=True)
    use_in_work = models.BooleanField(default=True)
    is_cookie_valid = models.BooleanField(default=None, null=True)

    def __str__(self):
        return self.name

    def check_cookie_file(self):
        jar = http.cookiejar.MozillaCookieJar(self.cookie.path)
        try:
            jar.load()
            self.is_cookie_valid = True
            self.save()
        except LoadError:
            self.is_cookie_valid = False
            self.save()
            raise LoadError

    def get_cookie(self):
        jar = http.cookiejar.MozillaCookieJar(self.cookie.path)
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
