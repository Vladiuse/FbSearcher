from django.db import models

class FbAccount(models.Model):
    name = models.CharField(max_length=50)
    cookie = models.FileField(upload_to='cookies')

    def __str__(self):
        return self.name


