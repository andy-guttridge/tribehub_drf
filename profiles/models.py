from django.db import models
from django.contrib.auth.models import User

from tribes.models import Tribe


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to='images/',
        default='../placeholder_profile_xnpcwj.webp'
    )
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
