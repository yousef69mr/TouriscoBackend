# Generated by Django 4.1.5 on 2023-07-06 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour_packages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourpackage',
            name='num_of_views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
