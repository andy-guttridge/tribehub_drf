from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

from tribes.models import Tribe


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='profile',
    )
    display_name = models.CharField(max_length=50)
    image = CloudinaryField(
        'image',
        default='../placeholder_profile_xnpcwj.webp'
    )
    tribe = models.ForeignKey(
        Tribe, on_delete=models.CASCADE,
        related_name='profile',
    )
    is_admin = models.BooleanField(default=False)
