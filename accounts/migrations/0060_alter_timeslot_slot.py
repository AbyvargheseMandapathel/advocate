# Generated by Django 4.2.4 on 2023-09-16 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0059_remove_timeslot_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='slot',
            field=models.CharField(choices=[('8-10', '8:00 AM - 10:00 AM'), ('10-12', '10:00 AM - 12:00 PM'), ('1-3', '1:00 PM - 3:00 PM'), ('3-5', '3:00 PM - 5:00 PM')], max_length=10),
        ),
    ]
