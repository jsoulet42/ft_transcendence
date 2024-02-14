import uuid
from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
	def create_user(self, username, list, password=None, **extra_fields):
		if not username:
			raise ValueError('The username field must be set')
		if not list:
			raise ValueError('The list field must be set')

		user = self.model(username=username, list=list, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		userlist, created = UsersList.objects.get_or_create(name = 'Superusers')
		return self.create_user(username, userlist, password, **extra_fields)


# Create your models here.
# Model = heritage d'une class django vierge personnalisable
class CustomUser(AbstractUser):
	USERNAME_FIELD = 'username'
	EMAIL_FILED = ''
	REQUIRED_FIELDS = []

	#CharField = model de string
	username = models.CharField(max_length = 50, unique = True, null = True)
	# UUIDField attribution d'un id non modifable
	uuid = models.UUIDField(default = uuid.uuid4, editable = False)
	# date de creation du user qui ne bouge pas si on met a jours le user
	join_date = models.DateField(auto_now = False, auto_now_add = True)
	# assignation du user a une list qui doit etre nommer a la creation du user et qui supprime tout les user si on delete la list
	photo_medium_url = models.URLField(max_length=255, blank=True)
	photo_small_url = models.URLField(max_length=255, blank=True)

	is_42_authenticated = models.BooleanField(default = False)

	list = models.ForeignKey("UsersList", null = False, on_delete = models.CASCADE, related_name = "users")

	objects = CustomUserManager()


class UsersList(models.Model):
	name = models.CharField(max_length = 255)

	def __str__(self):
		return f"{self.name}"

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
	host = models.ForeignKey("CustomUser", null = False, on_delete = models.CASCADE)

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
