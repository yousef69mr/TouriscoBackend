from django.db import models
from django.utils import timezone
from system.models import Language
# Create your models here.


def TourismCategoryImagesPath(instance, filename):
    return f'tourism_categories_images/{instance.name}/{filename}'


class TourismCategory(models.Model):
    name = models.CharField(default='', max_length=30, unique=True)
    image = models.ImageField(upload_to=TourismCategoryImagesPath)

    created = models.DateTimeField(
        default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return f'{self.name}'


class TourismCategoryLanguageBased(models.Model):
    lang = models.ForeignKey(
        Language, on_delete=models.CASCADE, verbose_name="language")
    categoryObject = models.ForeignKey(
        TourismCategory, on_delete=models.CASCADE, verbose_name="core")
    title = models.CharField(max_length=30)
    description = models.TextField()
    created = models.DateTimeField(
        default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)
    
    def __str__(self):
        return f'{self.title} => {self.lang.name}'

