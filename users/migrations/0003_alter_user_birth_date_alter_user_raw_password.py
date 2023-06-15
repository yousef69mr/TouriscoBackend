# Generated by Django 4.1.5 on 2023-06-14 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(null=True, verbose_name='Birth Date'),
        ),
        migrations.AlterField(
            model_name='user',
            name='raw_password',
            field=models.CharField(blank=True, help_text="You have to update and overwite this field value , If You successfully changed the User's password ONLY !!!", max_length=100),
        ),
    ]