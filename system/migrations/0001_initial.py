# Generated by Django 4.1.5 on 2023-05-05 21:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Example : [ar ,en,es]', max_length=3, unique=True, verbose_name='Language Code')),
                ('country_code', models.CharField(help_text='Example : [eg ,gb,sa,de]', max_length=3)),
                ('name', models.TextField()),
                ('dir', models.CharField(choices=[('rtl', 'Right to Left'), ('ltr', 'Left to Right')], max_length=3)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
                'ordering': ['id'],
            },
        ),
    ]
