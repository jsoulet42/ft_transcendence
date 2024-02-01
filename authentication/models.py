from django.db import models

# Create your models here.
class RequestCache(models.Model):
	state = models.CharField(max_length=32)

	class Meta:
		abstract = True
