from django.db import models

from tribes.models import Tribe


class Contact(models.Model):
    tribe = models.ForeignKey(
        Tribe, on_delete=models.CASCADE,
        related_name='tribe'
    )
    category = models.CharField(max_length=25, null=True, blank=True)
    company = models.CharField(max_length=25, null=True, blank=True)
    title = models.CharField(max_length=25, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
