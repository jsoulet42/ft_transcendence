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
	list_display = ("name", "get_users_name", "get_users_uuid", "get_users_join_date")
	search_fields = ("name",)

	def get_users_name(self, obj):
		return ", ".join([user.name for user in obj.users.all()])

	def get_users_uuid(self, obj):
		return ", ".join([str(user.uuid) for user in obj.users.all()])

	def get_users_join_date(self, obj):
		return ", ".join([str(user.join_date) for user in obj.users.all()])

	get_users_name.short_description = "User Names"
	get_users_uuid.short_description = "User UUIDs"
	get_users_join_date.short_description = "User Join Dates"
