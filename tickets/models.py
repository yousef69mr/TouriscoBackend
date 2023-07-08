from django.db import models
from django.utils import timezone
from landmark_events.models import LandmarkEvent
from system.models import Language
from categories.models import TicketClassCategory,TicketClassCategoryLanguageBased
# Create your models here.

# TICKETS_CATEGORIES = (
#     ('foreigner', 'Foreigner'),
#     ('foreigner student', 'foreigner Student'),
#     ('egyptian', 'Egyptian'),
#     ('arab', 'Arab'),
#     ('student', 'Student'),
#     ('أجنبي', 'أجنبى'),
#     ('طالب أجنبي', 'طالب أجنبى'),
#     ('مصري', 'مصرى'),
#     ('عرب', 'عربى'),
#     ('طالب', 'طالب')
# )


class Ticket(models.Model):
    name = models.CharField(default='', max_length=40)
    price = models.FloatField(help_text="Price in Egyptian Pounds")
    eventObject = models.ForeignKey(LandmarkEvent, on_delete=models.CASCADE, verbose_name="event")
    ticketClassObject = models.ForeignKey(TicketClassCategory,on_delete=models.CASCADE,verbose_name='ticket_class',default=1)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return f'{self.eventObject.name} => {self.price} LE'


class TicketLanguageBased(models.Model):
    ticketObject = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name="Ticket")
    lang = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="language")
    title = models.CharField(max_length=50)
    ticket_class_category = models.ForeignKey(TicketClassCategoryLanguageBased, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="category type")
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True, blank=False)

    def get_category_ticket_class(self):
        if not self.ticketObject:
            return None
        return TicketClassCategoryLanguageBased.objects.get(categoryObject=self.ticketObject.ticketClassObject,lang=self.lang)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.ticket_class_category and hasattr(self.ticketObject, 'ticketClassObject'):
            self.ticket_class_category = self.get_category_ticket_class()

    def __str__(self):
        return f'{self.lang.code} => {self.ticket_class_category.title} ({self.ticketObject.price} LE)'
