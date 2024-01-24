import uuid
from django.db import models

# Create your models here.
# Model = heritage d'une class django vierge personnalisable
class User(models.Model):
	#CharField = model de string
	name = models.CharField(max_length = 50)
	# UUIDField attribution d'un id non modifable
	uuid = models.UUIDField(default = uuid.uuid4, editable = False)
	# date de creation du user qui ne bouge pas si on met a jours le user
	join_date = models.DateField(auto_now = False, auto_now_add = True)
	# assignation du user a une list qui doit etre nommer a la creation du user et qui supprime tout les user si on delete la list
	list = models.ForeignKey("UsersList", null = False, on_delete = models.CASCADE)

class UsersList(models.Model):
	name = models.CharField(max_length = 255)
