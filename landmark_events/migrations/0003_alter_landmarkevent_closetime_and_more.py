# Generated by Django 4.1.5 on 2023-05-13 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmark_events', '0002_landmarkevent_closetime_landmarkevent_opentime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landmarkevent',
            name='closeTime',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='landmarkevent',
            name='openTime',
            field=models.TimeField(),
        ),
    ]