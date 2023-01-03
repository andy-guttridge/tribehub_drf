from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Specify fields to be accesible in admin panel for Profile model
    """
    list_display = ('user', 'display_name', 'is_admin')
