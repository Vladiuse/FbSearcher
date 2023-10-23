from django.db import models

# Create your models here.
class FbTemplate(models.Model):
    desc = models.CharField(
        max_length=255,
        blank=True
    )
    file = models.FileField(
        upload_to='fb_templates',
    )
    prev = models.URLField(
        blank=True,
    )

    @property
    def html(self):
        with open(self.file.path, encoding='utf-8') as file:
            return file.read()