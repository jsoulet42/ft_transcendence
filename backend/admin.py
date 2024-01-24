from backend.models import User,UsersList
from django.contrib import admin

# Register your models here.

class UserInline(admin.TabularInline):
	model = User
	extra = 0

@admin.register(User)
class userAdmin(admin.ModelAdmin):
	list_display = ("name", "uuid", "list", "join_date")
	list_filter = ("name","join_date")
	search_fields = ("name", )

@admin.register(UsersList)
class UsersListAdmin(admin.ModelAdmin):
	list_display = ("name",)
	list_filter = ("name",)
	search_fields = ("name", )
	inlines = (UserInline, )

