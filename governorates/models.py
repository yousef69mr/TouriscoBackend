from django.db import models
from django.utils import timezone
from system.models import Language

# Create your models here.

THEMES = (
    ('green', 'Green'),
    ('yellow', 'Yellow'),
    ('blue', 'Blue'),
    ('red', 'Red'),
    ('brown', 'Brown')
)


class Governorate(models.Model):
    name = models.CharField(default='', max_length=30, unique=True)
    emblem = models.ImageField(upload_to='emblems/%y/%m/%d')
    shape = models.TextField()
    area = models.FloatField(help_text="Squared Area in Km")
    theme = models.CharField(max_length=10, choices=THEMES)
    population = models.IntegerField(default=0)
    created = models.DateTimeField(
        default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return f'{self.name}'


class GovernorateLanguageBased(models.Model):
    govObject = models.ForeignKey(
        Governorate, related_name="governorates", on_delete=models.CASCADE, verbose_name="governorate")
    lang = models.ForeignKey(
        Language, on_delete=models.CASCADE, verbose_name="language")
    title = models.CharField(max_length=30)
    governor = models.CharField(max_length=70)
    description = models.TextField()

    created = models.DateTimeField(
        default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    class Meta:
        ordering = ['id']
        unique_together = (("govObject", "lang"),)

    def __str__(self):
        return f'{self.title} => {self.lang.name}'

