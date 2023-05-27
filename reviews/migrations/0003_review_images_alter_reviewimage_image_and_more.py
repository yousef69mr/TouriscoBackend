# Generated by Django 4.1.5 on 2023-05-25 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_image'),
        ('reviews', '0002_alter_review_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='images',
            field=models.ManyToManyField(through='reviews.ReviewImage', to='system.image'),
        ),
        migrations.AlterField(
            model_name='reviewimage',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.image'),
        ),
        migrations.AlterField(
            model_name='reviewimage',
            name='review',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='reviews.review'),
            preserve_default=False,
        ),
    ]