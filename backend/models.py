import uuid
from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.contrib.contenttypes.models import ContentType

class CustomUserManager(BaseUserManager):
	"""
	Custom user manager for managing CustomUser instances.

	Methods:
		create_user: Creates a regular user with the given username and userlist.
		create_superuser: Creates a superuser with the given username and password.
		create_dev: Creates a developer user with the given username and userlist.
	"""

	def create_user(self, username, userlist_name, password=None, **extra_fields):
		"""
		Creates a regular user with the given username and userlist name.
		Creates the userlist if not found.
		"""
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
		"""
		Creates a superuser with the given username and password.
		Creates the 'Superusers' Userslist if not found and assigns the new superuser
		to it.
		"""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self.create_user(username, 'Superusers', password, **extra_fields)

	def create_dev(self, username, userlist_name, password=None, **extra_fields):
		"""
		Creates a developer user with the given username and userlist.
		Creates the userlist if not found.
		Creates the 'Dev' group if not found and assigns the new user to it.
		"""
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

	def reset_stats(self, username):
		user = self.get(username=username)
		user.stats.games_played = 0
		user.stats.tournaments_played = 0
		user.stats.wins = 0
		user.stats.losses = 0
		user.stats.save()
		return user



# Create your models here.
# Model = heritage d'une class django vierge personnalisable
class CustomUser(AbstractUser):
	USERNAME_FIELD = 'username'
	EMAIL_FILED = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	nickname = models.CharField(max_length=50, blank=True, null=True)
	username = models.CharField(max_length=50, unique=True, null=True)
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)

	bio = models.CharField(max_length=2000, blank=True, null=True)
	github = models.URLField(max_length=255, blank=True)
	email = models.EmailField(max_length=254, blank=True)

	friends = models.ManyToManyField('self', blank=True)

	list = models.ForeignKey('UsersList', null=False, on_delete=models.CASCADE, related_name='users')

	games = models.ManyToManyField('Game', related_name='players', blank=True)
	tournaments = models.ManyToManyField('Tournament', related_name='players', blank=True)
	stats = models.OneToOneField('Stats', null=False, on_delete=models.CASCADE, related_name='user')

	campus = models.CharField(max_length=50, default='None')

	profile_image_path = models.CharField(max_length=255, blank=True, default='')
	photo_medium_url = models.URLField(max_length=255, blank=True)
	photo_small_url = models.URLField(max_length=255, blank=True)

	upload_image = models.ImageField(null=True, blank=True, upload_to='images')
	uploaded_image = models.CharField(max_length=255, blank=True, default='')

	def save(self, *args, **kwargs):
		# Check if the user is being created for the first time
		if not self.pk:
			stats = Stats.objects.create(
				games_played=0,
				tournaments_played=0,
				wins=0,
				losses=0
			)
			self.stats = stats
			stats.save()
		super().save(*args, **kwargs)


class FriendRequest(models.Model):
	"""
	Friend request sent between two users. The receiver can either accept or deny.
	If the receiver accepts, both users are added to each other's friends lists.
	If the receiver denies, the request is destroyed.
	"""
	STATUS_CHOICES = (
		('pending', 'Pending'),
		('accepted', 'Accepted'),
		('denied', 'Denied'),
	)

	sender = models.ForeignKey('CustomUser', related_name='sent_requests', on_delete=models.CASCADE)
	receiver = models.ForeignKey('CustomUser', related_name='received_requests', on_delete=models.CASCADE)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
	created_at = models.DateTimeField(auto_now_add=True)

class Stats(models.Model):
	"""
	Model with the data of a user's stats.
	Stores the number of games and tournaments played, the number of wins and the number of losses.
	"""
	games_played = models.PositiveSmallIntegerField(default=0)
	tournaments_played = models.PositiveSmallIntegerField(default=0)

	wins = models.PositiveSmallIntegerField(default=0)
	losses = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return f"{self.user.username} - Plays: {self.games_played} - Wins: {self.wins} - Losses: {self.losses} - Tournaments: {self.tournaments_played}"


class UsersList(models.Model):
	name = models.CharField(max_length = 255)

	def __str__(self):
		return f"{self.name}"


class Game(models.Model):
	"""
	Model with the data of a match.
	If the match is part of a tournament, the tournament field links to the its id.
	"""
	date = models.DateTimeField(auto_now=False, auto_now_add=True)
	game_duration = models.DurationField()

	host = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name="host")
	tournament = models.ForeignKey("Tournament", null=True, on_delete=models.CASCADE, related_name="tournament")

	player1 = models.CharField(max_length=50, null=False)
	player2 = models.CharField(max_length=50, null=False)

	player1_score = models.PositiveSmallIntegerField(default=0)
	player2_score = models.PositiveSmallIntegerField(default=0)


class Leaderboard(models.Model):
	"""
	Model with the data of a leaderboard.
	Stores a link to the logged in user and a list of all the players names in JSON format.
	"""
	host = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name="leaderboard_host")
	usernames = JSONField(default=list)

	def get_usernames(self):
		usernames_array = []
		for username in self.usernames:
			usernames_array.append(username)
		return usernames_array

	def set_usernames(self, usernames_list):
		"""
		Add usernames from the provided list to the existing JSON field.
		"""
		if not isinstance(usernames_list, list):
			raise ValueError("Input must be a list of usernames")

		existing_usernames = self.usernames or []
		existing_usernames.extend(usernames_list)

		self.usernames = existing_usernames


class Tournament(models.Model):
	"""
	Model with the data of a tournament.
	Stores the host of the tournament, the number of players, the date of the tournament and the leaderboard.
	The number of players can only be 4 or 8.
	"""
	CHOICE_OPTION1 = 4
	CHOICE_OPTION2 = 8

	COUNT_CHOICES = (
		(CHOICE_OPTION1, 4),
		(CHOICE_OPTION2, 8),
	)

	name = models.CharField(max_length=50, null=False)
	date = models.DateTimeField(auto_now=False, auto_now_add=True)

	players_count = models.PositiveSmallIntegerField(choices=COUNT_CHOICES, default=CHOICE_OPTION1)
	leaderboard = models.ForeignKey("Leaderboard", null=True, on_delete=models.CASCADE, related_name="leaderboard")

	games = models.ManyToManyField("Game", related_name="tournament_games")

	def __str__(self):
		return f"{self.name} - {self.date} -- Leaderboard: {self.leaderboard.get_usernames()}"
