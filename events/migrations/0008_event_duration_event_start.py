# Generated by Django 4.1.4 on 2023-01-03 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_remove_event_recurrences'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='duration',
            field=models.DurationField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='start',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]
