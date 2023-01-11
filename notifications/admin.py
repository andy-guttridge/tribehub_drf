from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Specify fields to be accesible in admin panel for Profile model
    """
    list_display = (
        'user',
        'date_created',
        'subject',
        'message',
        'type',
        'event',
    )
