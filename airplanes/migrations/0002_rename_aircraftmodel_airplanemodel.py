# Generated by Django 4.1.5 on 2023-04-06 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("airplanes", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="aircraftModel",
            new_name="AirplaneModel",
        ),
    ]
