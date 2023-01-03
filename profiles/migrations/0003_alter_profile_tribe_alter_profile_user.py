# Generated by Django 4.1.4 on 2023-01-03 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tribes', '0002_tribe_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0002_alter_profile_tribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='tribe',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='tribes.tribe'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
