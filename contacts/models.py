from django.db import models

from tribes.models import Tribe


class Contact(models.Model):
    tribe = models.ForeignKey(
        Tribe, on_delete=models.CASCADE,
        related_name='tribe'
    )
    category = models.CharField(max_length=25)
    title = models.CharField(max_length=25)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(null=True)
