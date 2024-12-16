from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username', 'first_name', 'last_name', 'date_joined')

# Register the UserProfile model with the custom admin class
admin.site.register(User, UserAdmin)