# Generated by Django 4.1.5 on 2023-06-24 01:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_ticketclasscategory_ticketclasscategorylanguagebased'),
        ('landmarks', '0005_landmark_coordinates_alter_landmark_height'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandmarkTourismCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
                ('active', models.BooleanField(default=True)),
                ('categoryObject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.tourismcategory', verbose_name='Tourism Category')),
                ('landmarkObject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landmarks.landmark', verbose_name='landmark')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('landmarkObject', 'categoryObject')},
            },
        ),
        migrations.AddField(
            model_name='landmark',
            name='tourism_categories',
            field=models.ManyToManyField(related_name='landmark_tourism_categories', through='landmarks.LandmarkTourismCategory', to='categories.tourismcategory'),
        ),
    ]