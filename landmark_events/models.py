from django.db import models
from django.utils import timezone
from landmarks.models import Landmark
from system.models import Language

# Create your models here.



class LandmarkEvent(models.Model):
    name = models.CharField(default='', max_length=70)
    landmarkObject = models.ForeignKey(Landmark, on_delete=models.CASCADE, verbose_name="landmark")
    
    isMain = models.BooleanField(default=False)
    is_eternel = models.BooleanField(default=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default='9999-12-30 23:59:59.314354+00:00')
    openTime = models.TimeField()
    closeTime = models.TimeField()
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    

    class Meta:
        ordering = ['id']
        unique_together = (("name", "landmarkObject"),)

    def __str__(self):
        # landmark = get_object_or_404(LandmarkLanguageBased, place=self.place.id)
        return f'{self.name} => ({self.landmarkObject})'


class LandmarkEventLanguageBased(models.Model):
    title = models.CharField(max_length=70)
    lang = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="language")
    eventObject = models.ForeignKey(LandmarkEvent, on_delete=models.CASCADE, verbose_name="Event")

    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    class Meta:
        ordering = ['id']
        unique_together = (("eventObject", "lang"),)

    def __str__(self):
        return f'{self.title} => {self.lang.name}'

