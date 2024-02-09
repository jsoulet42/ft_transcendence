from backend.models import CustomUser,UsersList
from django.contrib import admin

# Register your models here.

class UserInline(admin.TabularInline):
	model = CustomUser
	extra = 0

@admin.register(CustomUser)
class userAdmin(admin.ModelAdmin):
	list_display = ("name", "uuid", "list", "join_date", "photo_medium_url", "photo_small_url")
	list_filter = ("name","join_date")
	search_fields = ("name", )

@admin.register(UsersList)
class UsersListAdmin(admin.ModelAdmin):
	list_display = ("name", "get_users_name")
	search_fields = ("name",)

	def get_users_name(self, obj):
		return " | ".join([user.name for user in obj.users.all()])

	get_users_name.short_description = "User Names"
