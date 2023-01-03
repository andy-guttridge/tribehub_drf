from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Specify fields to be accesible in admin panel for Profile model
    """
    list_display = (
        'user',
        'tribe',
        'get_to',
        'start',
        'duration',
        'recurrence_type',
        'subject',
        'category',
        # 'accepted',
    )

    def get_to(self, obj):
        """
        Create a string of the users invited to this event
        """
        # Approach to creating a string representation of a many-to-many field
        # adapted from
        # https://stackoverflow.com/questions/18108521/many-to-many-in-list-display-django
        string = ''
        for user in obj.to.all():
            string += str(f'{user.username}, ')
        return string
