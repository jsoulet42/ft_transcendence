from django.db import models

# Create your models here.
class Request_cache(models.Model):
    state = models.CharField(max_length = 32, null = False)