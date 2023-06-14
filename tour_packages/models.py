from django.db import models
from users.models import User
from django.utils import timezone
from landmark_events.models import LandmarkEvent
from categories.models import TourismCategory
from tickets.models import TicketLanguageBased

# Create your models here.

class TourPackage(models.Model):
    title = models.CharField(max_length=150)
    user_created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    events = models.ManyToManyField(LandmarkEvent,related_name='events')
    tourism_categories = models.ManyToManyField(TourismCategory,related_name='tourism_categories',through='TourPackageTourismCategory')
    package_maximium_budget = models.FloatField()
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
    
    # def calculate_total_price(self):
    #     total_cost = 0
        
    #     for event in self.events.all():

    #         if self.user_created_by.nationality == 'EG':
    #             category = 'egyptian'
    #         elif self.user_created_by.nationality in ['UAE','SA']:
    #             category = 'arab'
    #         else:
    #             category = 'foreigner'
    #         ticket = TicketLanguageBased.objects.get(ticketObject__eventObject=event,category=category)
    #         total_cost+= ticket.ticketObject.price
    #     return total_cost
                
            
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if not self.package_maximium_budget and hasattr(self, 'events'):
    #         self.package_maximium_budget = self.calculate_total_price()

            
    def __str__(self):

        return f'{self.title}'

class TourPackageTourismCategory(models.Model):
    tourism_category = models.ForeignKey(TourismCategory,on_delete=models.CASCADE)
    tourpackage = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.tourpackage.title} => {self.tourism_category.name}'

# # class UserTourPackage(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     tourpackage = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
#     created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
#     active = models.BooleanField(default=True)