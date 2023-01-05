# Generated by Django 4.1.4 on 2023-01-05 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_event_accepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='recurrence_type',
            field=models.CharField(choices=[('NON', 'None'), ('REC', 'Is Recurrence'), ('DAI', 'Daily'), ('WEK', 'Weekly'), ('TWK', 'Two weekly'), ('MON', 'Monthly'), ('YEA', 'Yearly')], default='NON', max_length=3),
        ),
    ]
