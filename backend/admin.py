from backend.models import CustomUser, UsersList, Stats, Game, Tournament, Leaderboard
from django.contrib import admin

# Register your models here.

class UserInline(admin.TabularInline):
	model = CustomUser
	extra = 0


@admin.register(CustomUser)
class userAdmin(admin.ModelAdmin):
	list_display = ("username", "uuid", "list", "date_joined", "nickname", "photo_medium_url", "photo_small_url")
	list_filter = ("username","date_joined")
	search_fields = ("username", )


@admin.register(UsersList)
class UsersListAdmin(admin.ModelAdmin):
	list_display = ("name", "get_users_name")
	search_fields = ("name",)

	def get_users_name(self, obj):
		return " | ".join([user.username for user in obj.users.all()])

	get_users_name.short_description = "Usernames"


@admin.register(Stats)
class StatsAdmin(admin.ModelAdmin):
	list_display = ("user", "games_played", "tournaments_played", "wins", "losses")
	search_fields = ("user",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
	list_display = ("host", "game_duration", "player1", "player2", "player1_score", "player2_score")
	search_fields = ("host", "player1", "player2")


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
	list_display = ("name", "date", "get_players_name")
	search_fields = ("name",)

	def get_players_name(self, obj):
		return " | ".join(obj.leaderboard.get_usernames())

	get_players_name.short_description = "Leaderboard"


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
	list_display = ("host", "get_usernames")
	search_fields = ("host",)

	def get_usernames(self, obj):
		return " | ".join(obj.get_usernames())

	get_usernames.short_description = "Usernames"
