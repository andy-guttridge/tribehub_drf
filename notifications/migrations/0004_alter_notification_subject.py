# Generated by Django 4.1.4 on 2023-03-09 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_rename_to_user_notification_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='subject',
            field=models.CharField(max_length=100),
        ),
    ]
