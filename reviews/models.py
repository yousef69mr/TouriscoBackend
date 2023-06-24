from django.db import models
from django.apps import apps
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from users.models import User
from system.models import Image


# Create your models here.

# def ReviewImagesPath(instance, filename):
#     return f'reviews_images/{instance.review.id}/{filename}'

# def get_reviewable_models():
#     reviewable_models = []
#     for app_label in ['landmarks', 'landmark_events']:
#         app_models = apps.get_app_config(app_label).get_models()
#         for model in app_models:
#             if hasattr(model, 'reviews' ):
#                 content_type = ContentType.objects.get_for_model(model)
#                 reviewable_models.append(Q(content_type=content_type))
#     return reviewable_models

class Review(models.Model):
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(blank=True,null=True)
    images = models.ManyToManyField(Image,through='ReviewImage')
    userObject = models.ForeignKey(User,on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'app_label__in': ['landmarks', 'landmark_events']})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created']

    def __str__(self):
        return f'#{self.id} ) {self.userObject.username} => {self.rating}'
    
class ReviewImage(models.Model):
    review = models.ForeignKey(Review,on_delete=models.CASCADE)
    image = models.ForeignKey(Image,on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    class Meta:
        ordering = ['-created']
        verbose_name = "Review Image"
        verbose_name_plural = "Review Images"

    def __str__(self):
        return f'#{self.id} => {self.review}'