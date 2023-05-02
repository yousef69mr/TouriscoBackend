# Generated by Django 4.1.5 on 2023-02-20 01:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Governorate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=30)),
                ('emblem', models.ImageField(upload_to='emblems/%y/%m/%d')),
                ('shape', models.TextField()),
                ('area', models.FloatField(help_text='Squared Area in Km')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Landmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='landmark_images/%y/%m/%d')),
                ('area', models.FloatField(help_text='Squared Area in metre')),
                ('location', models.CharField(help_text='google maps link ', max_length=200)),
                ('height', models.FloatField(default=1, help_text='height in metre')),
                ('foundationDate', models.DateField(default=django.utils.timezone.now, verbose_name='Foundation Date')),
                ('foundationDateEra', models.CharField(choices=[('BC', 'BC'), ('AD', 'AD')], default='AD', max_length=3, verbose_name='Foundation Date Era')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
                ('active', models.BooleanField(default=True)),
                ('governorate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.governorate')),
            ],
        ),
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
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(help_text='Price in Egyptian Pounds')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
                ('active', models.BooleanField(default=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.landmark', verbose_name='landmark')),
            ],
        ),
        migrations.CreateModel(
            name='TicketLanguageBased',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('foreginer', 'Foreginer'), ('foreginerStudent', 'Foreginer Student'), ('egyptian', 'Egyptian'), ('arab', 'Arab'), ('student', 'Student'), ('أجنبى', 'أجنبى'), ('طالب_أجنبى', 'طالب أجنبى'), ('مصرى', 'مصرى'), ('عربى', 'عربى'), ('طالب', 'طالب')], max_length=20)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
                ('active', models.BooleanField(default=True)),
                ('lang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.language', verbose_name='language')),
                ('ticketObject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.ticket', verbose_name='Ticket')),
            ],
        ),
        migrations.CreateModel(
            name='LandmarkLanguageBased',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('founder', models.CharField(max_length=70)),
                ('description', models.TextField()),
                ('address', models.TextField(max_length=300)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
                ('active', models.BooleanField(default=True)),
                ('lang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.language', verbose_name='language')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landmarks', to='system.landmark', verbose_name='landmark')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('place', 'lang')},
            },
        ),
        migrations.CreateModel(
            name='GovernorateLanguageBased',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('governor', models.CharField(max_length=70)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
                ('active', models.BooleanField(default=True)),
                ('gov', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='governorates', to='system.governorate', verbose_name='governorate')),
                ('lang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.language', verbose_name='language')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('gov', 'lang')},
            },
        ),
    ]