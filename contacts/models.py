from django.db import models

from tribes.models import Tribe


class Contact(models.Model):
    tribe = models.ForeignKey(
        Tribe, on_delete=models.CASCADE,
        related_name='tribe'
    )
    category = models.CharField(max_length=25, null=True)
    title = models.CharField(max_length=25, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
