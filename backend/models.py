import uuid
from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.contrib.contenttypes.models import ContentType

class CustomUserManager(BaseUserManager):
	def create_user(self, username, userlist_name, password=None, **extra_fields):
		if not username:
			raise ValueError('The username field must be set')
		if not userlist_name:
			raise ValueError('The list field must be set')

		userlist, created = UsersList.objects.get_or_create(name=userlist_name)

		user = self.model(username=username, list=userlist, **extra_fields)
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

		return self.create_user(username, 'Superusers', password, **extra_fields)

	def create_dev(self, username, userlist_name, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Dev user must have is_staff=True.')

		dev_user = self.create_user(username, userlist_name, password)

		dev_group, created = Group.objects.get_or_create(name='Dev')

		admin_content_type = ContentType.objects.get_for_model(CustomUser)
		admin_permissions = Permission.objects.filter(content_type=admin_content_type)
		dev_group.permissions.add(*admin_permissions)

		dev_user.groups.add(dev_group)
		return dev_user


# Create your models here.
# Model = heritage d'une class django vierge personnalisable
class CustomUser(AbstractUser):
	USERNAME_FIELD = 'username'
	EMAIL_FILED = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	#CharField = model de string
	username = models.CharField(max_length=50, unique=True, null=True)
	# UUIDField attribution d'un id non modifable
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)

	bio = models.CharField(max_length=2000, blank=True, null=True)

	github = models.URLField(max_length=255, blank=True)

	email = models.EmailField(max_length=254, blank=True)

	# assignation du user a une list qui doit etre nommer a la creation du user et qui supprime tout les user si on delete la list
	list = models.ForeignKey("UsersList", null=False, on_delete=models.CASCADE, related_name="users")

	# 42 related data
	campus = models.CharField(max_length=50, default="None")

	photo_medium_url = models.URLField(max_length=255, blank=True)
	photo_small_url = models.URLField(max_length=255, blank=True)

	upload_image = models.ImageField(null=True, blank=True, upload_to='images')

	profile_image_path = models.CharField(max_length=255, blank=True, default='')

	uploaded_image = models.CharField(max_length=255, blank=True, default='')

	nickname = models.CharField(max_length=50, blank=True, null=True)

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