from django.db import models
from django.utils import timezone
from system.models import Language
# Create your models here.


def TourismCategoryImagesPath(instance, filename):
    return f'tourism_categories_images/{instance.name}/{filename}'


class TourismCategory(models.Model):
    name = models.CharField(default='', max_length=30, unique=True)
    image = models.ImageField(default='defaults/tourism_category_default.jpg', upload_to=TourismCategoryImagesPath)

    created = models.DateTimeField(
        default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    class Meta:
        verbose_name = 'Tourism Category'
        verbose_name_plural = 'Tourism Categories'

    def __str__(self):
        return f'{self.name}'


class TourismCategoryLanguageBased(models.Model):
    lang = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="language")
    categoryObject = models.ForeignKey(TourismCategory, on_delete=models.CASCADE, verbose_name="core")
    title = models.CharField(max_length=30)
    description = models.TextField()
    created = models.DateTimeField(
        default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)
    
    def __str__(self):
        return f'{self.title} => {self.lang.name}'


class TypeCategory(models.Model):
    name = models.CharField(default='', max_length=30, unique=True)

    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    class Meta:
        verbose_name = 'Type Category'
        verbose_name_plural = 'Type Categories'

    def __str__(self):
        return f'{self.name}'


class TypeCategoryLanguageBased(models.Model):
    lang = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="language")
    categoryObject = models.ForeignKey(TypeCategory, on_delete=models.CASCADE, verbose_name="core")
    title = models.CharField(max_length=70)
    description = models.TextField(null=True,blank=True)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.title} => {self.lang.name}'



class TicketClassCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Ticket Class Category'
        verbose_name_plural = 'Ticket Class Categories'

    def __str__(self):
        return f'{self.name}'


class TicketClassCategoryLanguageBased(models.Model):
    lang = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="language")
    categoryObject = models.ForeignKey(TicketClassCategory, on_delete=models.CASCADE, verbose_name="core")
    title = models.CharField(max_length=50)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)
    
    def __str__(self):
        return f'{self.title} => {self.lang.name}'
