from django.utils import timezone
import os
from django.db import models
from users.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.

DIRECTIONS = (
    ("rtl", "Right to Left"),
    ("ltr", "Left to Right")
)

ERAS = (
    ("BC", "BC"),
    ("AD", "AD")
)

def ImagePath(instance,filename):
    if hasattr(instance.content_object,'name'):
        return f'{instance.content_object._meta.app_label}_images/{instance.content_object.name}/{filename}'
    return f'{instance.content_object._meta.app_label}_images/#{instance.content_object.id}/{filename}'

class Language(models.Model):
    code = models.CharField(unique=True, help_text="Example : [ar ,en,es]", max_length=3, verbose_name="Language Code")
    country_code = models.CharField(help_text="Example : [eg ,gb,sa,de]", max_length=3)
    name = models.TextField()
    dir = models.CharField(choices=DIRECTIONS, max_length=3)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} ({self.country_code})'


class Image(models.Model):
    userObject = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'app_label__in': ['landmarks', 'landmark_events','reviews']})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=ImagePath)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        ordering = ['-created']
    
    def __str__(self):
        if hasattr(self.content_object,'name'):
            return f'{self.content_object.name} => {os.path.basename(self.image.name)}'
        elif hasattr(self.content_object,'id'):
            return f'#{self.content_object.id} => {os.path.basename(self.image.name)}'
        else:
            return f'{os.path.basename(self.image.name)}'

class Coordinate(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=7)
    longitude = models.DecimalField(max_digits=9, decimal_places=7)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}"


# def LandmarkImagesPath(instance, filename):
#     return f'landmark_images/{instance.name}/{filename}'


# class Landmark(models.Model):
#     name = models.CharField(default='', max_length=40, unique=True)
#     image = models.ImageField(
#         upload_to=LandmarkImagesPath)
#     tourismCategoryObject =models.ForeignKey(TourismCategory,on_delete=models.CASCADE)
#     area = models.FloatField(help_text="Squared Area in metre")
#     location = models.CharField(max_length=200, help_text="google maps link ")
#     govObject = models.ForeignKey(Governorate, on_delete=models.CASCADE)
#     height = models.FloatField(default=1, help_text="height in metre")
#     foundationDate = models.DateField(
#         default=timezone.now, verbose_name="Foundation Date")
#     foundationDateEra = models.CharField(
#         choices=ERAS, max_length=3, default='AD', verbose_name="Foundation Date Era")
#     created = models.DateTimeField(
#         default=timezone.now, verbose_name="Creation Date")
#     active = models.BooleanField(default=True, blank=False)

#     def __str__(self):
#         return self.name


# class TourismTypesLandmarkList(models.Model):
#     landmarkObject = models.ForeignKey(
#         Landmark, on_delete=models.CASCADE, verbose_name="landmark")
#     categoryObject = models.ForeignKey(
#         TourismCategory, on_delete=models.CASCADE, verbose_name="core")

#     def __str__(self):
#         return f'{self.landmarkObject.name} == {self.categoryObject.name}'


# class LandmarkImage(models.Model):
#     landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE)
#     image = models.ImageField(
#         upload_to=landmark.id)

#     def __str__(self):
#         return f'{self.landmark.title} image'


# class LandmarkLanguageBased(models.Model):
#     landmarkObject = models.ForeignKey(
#         Landmark, on_delete=models.CASCADE, verbose_name="landmark")
#     lang = models.ForeignKey(
#         Language, on_delete=models.CASCADE, verbose_name="language")
#     title = models.CharField(max_length=30)
#     founder = models.CharField(max_length=70, null=True, blank=True)
#     description = models.TextField()
#     address = models.TextField(max_length=300)
#     # foreignersPrice = models.FloatField(help_text="price in Egyptian Pound")
#     # localPrice = models.FloatField(help_text="price in Egyptian Pound")

#     created = models.DateTimeField(
#         default=timezone.now, verbose_name="Creation Date")
#     active = models.BooleanField(default=True, blank=False)

#     class Meta:
#         ordering = ['id']
#         unique_together = (("landmarkObject", "lang"),)

#     def __str__(self):
#         return f'{self.title} => {self.lang.name}'

########################################################
