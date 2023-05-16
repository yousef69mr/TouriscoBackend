from django.db import models
from django.utils import timezone
from landmark_events.models import LandmarkEvent
from system.models import Language
# Create your models here.

TICKETS_CATEGORIES = (
    ('foreigner', 'Foreigner'),
    ('foreigner student', 'foreigner Student'),
    ('egyptian', 'Egyptian'),
    ('arab', 'Arab'),
    ('student', 'Student'),
    ('أجنبي', 'أجنبى'),
    ('طالب أجنبي', 'طالب أجنبى'),
    ('مصري', 'مصرى'),
    ('عرب', 'عربى'),
    ('طالب', 'طالب')
)


class Ticket(models.Model):
    name = models.CharField(default='', max_length=40)
    price = models.FloatField(help_text="Price in Egyptian Pounds")
    eventObject = models.ForeignKey(
        LandmarkEvent, on_delete=models.CASCADE, verbose_name="event")
    created = models.DateTimeField(
        default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return f'{self.eventObject.name} => {self.price} LE'


class TicketLanguageBased(models.Model):
    ticketObject = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, verbose_name="Ticket")
    lang = models.ForeignKey(
        Language, on_delete=models.CASCADE, verbose_name="language")
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=TICKETS_CATEGORIES)
    created = models.DateTimeField(
        default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return f'{self.lang.code} => {self.category} ({self.ticketObject.price} LE)'
