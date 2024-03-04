from django.db import models


class RequestCache(models.Model):
    state = models.CharField(max_length=32)

    class Meta:
        abstract = True
