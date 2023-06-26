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


