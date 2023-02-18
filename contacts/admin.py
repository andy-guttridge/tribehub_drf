from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Specify fields to be accesible in admin panel for Profile model
    """
    list_display = (
        'tribe',
        'company',
        'category',
        'title',
        'first_name',
        'last_name',
        'phone',
        'email',
    )
