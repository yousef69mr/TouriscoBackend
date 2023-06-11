# Generated by Django 4.2.1 on 2023-06-11 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourism_categories', '0006_typecategory_typecategorylanguagebased'),
        ('landmarks', '0009_landmark_user_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='landmark',
            name='typeCategoryObject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tourism_categories.typecategory'),
        ),
    ]