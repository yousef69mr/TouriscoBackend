# Generated by Django 4.1.5 on 2023-06-14 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmarks', '0002_alter_landmark_location_link'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TourismTypesLandmarkList',
        ),
    ]