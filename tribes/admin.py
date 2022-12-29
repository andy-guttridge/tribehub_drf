from django.contrib import admin
from django.db import models
from .models import Tribe


@admin.register(Tribe)
class TribeAdmin(admin.ModelAdmin):
    """
    Specify fields to be accesible in admin panel for Tribe model
    """
    list_display = ('name',)
