# Generated by Django 4.1.4 on 2022-12-29 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tribes', '0002_tribe_name'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='tribe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='tribes.tribe'),
        ),
    ]
