# Generated by Django 4.1.4 on 2023-01-03 11:23

from django.db import migrations
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_rename_repeat_event_recurrence_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='recurrences',
            field=recurrence.fields.RecurrenceField(default=None, null=True),
        ),
    ]
