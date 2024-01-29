import uuid
from django.db import models
from django.db.models import JSONField

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

# models.ManyToManyField()
class Tournament(models.Model):
	CHOICE_OPTION1 = 4
	CHOICE_OPTION2 = 8
	
	COUNT_CHOICES = (
		(CHOICE_OPTION1, 4),
		(CHOICE_OPTION2, 8),
	)
	
	DEFAULT_NAME = 'Unknown'

	name = models.CharField(max_length = 50)
	date = models.DateField(auto_now = False, auto_now_add = True)
	host = models.ForeignKey("User", null = False, on_delete = models.CASCADE)
	
	players_count = models.PositiveSmallIntegerField(default = 8, choices = COUNT_CHOICES)
	
	leaderboard = JSONField(default = list)

	def add_leaderboard_user(self, new_user_name, position=0):
		if self.leaderboard == []:
			self.leaderboard.append(new_user_name)
			self.save()
			return self
		leaderboard_len = len(self.leaderboard)
		if leaderboard_len > self.players_count:
			return self
		if position > leaderboard_len or position <= 0:
			self.leaderboard.append(new_user_name)
			self.save()
			return self
		self.leaderboard.insert(position, new_user_name)
		self.save()
		return self