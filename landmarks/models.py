from django.db import models
from django.utils import timezone
# import os
from categories.models import TourismCategory,TypeCategory,TypeCategoryLanguageBased
from system.models import Language,Image
from governorates.models import Governorate
from reviews.models import Review
from users.models import User



# Create your models here.

def LandmarkImagesPath(instance, filename):
    # print(instance.id)
    # if instance.id:
    #     return f'landmarks_images/{instance.name}_#{str(instance.id)}/{filename}'
    # else:
    return f'landmarks_images/{instance.name}/{filename}'



ERAS = (
    ("BC", "BC"),
    ("AD", "AD")
)


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
    image = models.ImageField(default='defaults/landmark_default.jpg',upload_to=LandmarkImagesPath)
    tourismCategoryObject = models.ForeignKey(TourismCategory,on_delete=models.SET_NULL, null=True)
    typeCategoryObject = models.ForeignKey(TypeCategory,on_delete=models.CASCADE,default=1)
    images= models.ManyToManyField(Image,through='LandmarkImage',blank=True)
    reviews = models.ManyToManyField(Review,through='LandmarkReview',blank=True)
    user_created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    area = models.FloatField(help_text="Squared Area in metre")
    location_link = models.URLField( help_text="google maps link ",max_length=500)
    govObject = models.ForeignKey(Governorate, on_delete=models.CASCADE)
    
    height = models.FloatField(default=1, help_text="height in metre")
    foundationDate = models.DateField(default=timezone.now, verbose_name="Foundation Date")
    foundationDateEra = models.CharField(choices=ERAS, max_length=3, default='AD', verbose_name="Foundation Date Era")
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)
   
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if 'temp' in self.image.name:
    #         # Move the image to the correct path now that we have an ID
    #         new_path = LandmarkImagesPath(self, self.image.name.split('/')[-1])
    #         print(new_path)
    #         os.rename(self.image.path, new_path)
    #         self.image.name = new_path
    #         self.save(update_fields=['image'])

    def __str__(self):
        return self.name

class LandmarkImage(models.Model):
    landmark = models.ForeignKey(Landmark,on_delete=models.CASCADE)
    image = models.ForeignKey(Image,on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    class Meta:
        ordering = ['-created']
        unique_together = [('landmark','image')]
        verbose_name = "Landmark Image"
        verbose_name_plural = "Landmark Images"

    def __str__(self):
        return f'{self.landmark.name} => {self.image.image}'
    
class LandmarkReview(models.Model):
    landmark = models.ForeignKey(Landmark,on_delete=models.CASCADE)
    review = models.ForeignKey(Review,on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    class Meta:
        ordering = ['-created']
        unique_together = [('landmark','review')]
        verbose_name = "Landmark Review"
        verbose_name_plural = "Landmark Reviews"

    def __str__(self):
        return f'#{self.landmark.name} => {self.review.rating}'


class LandmarkLanguageBased(models.Model):
    
    landmarkObject = models.ForeignKey(Landmark, on_delete=models.CASCADE, verbose_name="landmark")
    lang = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="language")
    title = models.CharField(max_length=30)
    founder = models.CharField(max_length=70, null=True, blank=True)
    description = models.TextField()
    category_type = models.ForeignKey(TypeCategoryLanguageBased, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="category type")
    address = models.TextField(max_length=300)
    # foreignersPrice = models.FloatField(help_text="price in Egyptian Pound")
    # localPrice = models.FloatField(help_text="price in Egyptian Pound")

    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
        unique_together = (("landmarkObject", "lang"),)
    
    def get_category_type(self):
        return TypeCategoryLanguageBased.objects.get(categoryObject=self.landmarkObject.typeCategoryObject,lang=self.lang)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.category_type and hasattr(self.landmarkObject, 'typeCategoryObject'):
            self.category_type = self.get_category_type()

    def __str__(self):
        return f'{self.title} => {self.lang.name}'
    
# many to many relation not used
# class TourismTypesLandmarkList(models.Model):
#     landmarkObject = models.ForeignKey(
#         Landmark, on_delete=models.CASCADE, verbose_name="landmark")
#     categoryObject = models.ForeignKey(
#         TourismCategory, on_delete=models.CASCADE, verbose_name="core")

#     def __str__(self):
#         return f'{self.landmarkObject.name} == {self.categoryObject.name}'

