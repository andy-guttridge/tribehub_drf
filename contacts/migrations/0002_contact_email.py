# Generated by Django 4.1.4 on 2023-01-11 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
