from django.db import models
from django.utils import timezone
from tourism_categories.models import TourismCategory
from system.models import Language
from governorates.models import Governorate


# Create your models here.

def LandmarkImagesPath(instance, filename):
    return f'landmark_images/{instance.name}/{filename}'


ERAS = (
    ("BC", "BC"),
    ("AD", "AD")
)


# class Landmark(models.Model):
#     name = models.CharField(default='', max_length=100, unique=True)
#     image = models.ImageField(default='defaults/landmark_default.jpg',
#         upload_to=LandmarkImagesPath)
#     tourismCategoryObject = models.ManyToManyField(TourismCategory,through='LandmarkWithTourismCategoryList')
#     area = models.FloatField(help_text="Squared Area in metre")
#     location = models.TextField( help_text="google maps link ")
#     govObject = models.ForeignKey(Governorate, on_delete=models.CASCADE)
#     height = models.FloatField(default=1, help_text="height in metre")
#     foundationDate = models.DateField(
#         default=timezone.now, verbose_name="Foundation Date")
#     foundationDateEra = models.CharField(
#         choices=ERAS, max_length=3, default='AD', verbose_name="Foundation Date Era")
#     created = models.DateTimeField(
#         default=timezone.now, verbose_name="Creation Date")
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name
    

# class LandmarkWithTourismCategoryList(models.Model):
#     landmarkObject = models.ForeignKey(
#         Landmark, on_delete=models.CASCADE, verbose_name="landmark")
#     categoryObject = models.ForeignKey(
#         TourismCategory, on_delete=models.CASCADE, verbose_name="core")
#     created = models.DateTimeField(
#         default=timezone.now, verbose_name="Creation Date")
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return f'{self.landmarkObject.name} == {self.categoryObject.name}'



class Landmark(models.Model):
    name = models.CharField(default='', max_length=100, unique=True)
    image = models.ImageField(default='defaults/landmark_default.jpg',
        upload_to=LandmarkImagesPath)
    tourismCategoryObject = models.ForeignKey(TourismCategory,on_delete=models.CASCADE)
    area = models.FloatField(help_text="Squared Area in metre")
    location = models.TextField( help_text="google maps link ")
    govObject = models.ForeignKey(Governorate, on_delete=models.CASCADE)
    height = models.FloatField(default=1, help_text="height in metre")
    foundationDate = models.DateField(
        default=timezone.now, verbose_name="Foundation Date")
    foundationDateEra = models.CharField(
        choices=ERAS, max_length=3, default='AD', verbose_name="Foundation Date Era")
    created = models.DateTimeField(
        default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class LandmarkLanguageBased(models.Model):
    landmarkObject = models.ForeignKey(
        Landmark, on_delete=models.CASCADE, verbose_name="landmark")
    lang = models.ForeignKey(
        Language, on_delete=models.CASCADE, verbose_name="language")
    title = models.CharField(max_length=30)
    founder = models.CharField(max_length=70, null=True, blank=True)
    description = models.TextField()
    address = models.TextField(max_length=300)
    # foreignersPrice = models.FloatField(help_text="price in Egyptian Pound")
    # localPrice = models.FloatField(help_text="price in Egyptian Pound")

    created = models.DateTimeField(
        default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
        unique_together = (("landmarkObject", "lang"),)

    def __str__(self):
        return f'{self.title} => {self.lang.name}'
    

class TourismTypesLandmarkList(models.Model):
    landmarkObject = models.ForeignKey(
        Landmark, on_delete=models.CASCADE, verbose_name="landmark")
    categoryObject = models.ForeignKey(
        TourismCategory, on_delete=models.CASCADE, verbose_name="core")

    def __str__(self):
        return f'{self.landmarkObject.name} == {self.categoryObject.name}'

