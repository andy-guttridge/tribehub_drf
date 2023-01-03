# Generated by Django 4.1.4 on 2023-01-03 12:15

from django.db import migrations
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_event_duration_event_start'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='accepted',
        ),
        migrations.AddField(
            model_name='event',
            name='recurrences',
            field=recurrence.fields.RecurrenceField(blank=True, null=True),
        ),
    ]