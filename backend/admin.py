from backend.models import CustomUser,UsersList
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
