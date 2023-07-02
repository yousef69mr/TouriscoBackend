from django.db import models
from users.models import User
from django.db.models import Sum
from django.utils import timezone
from landmark_events.models import LandmarkEvent
from categories.models import TourismCategory
from tickets.models import Ticket

# Create your models here.

class TourPackage(models.Model):
    title = models.CharField(max_length=150)
    user_created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    tickets = models.ManyToManyField(Ticket,related_name='tickets',through='TourPackageTicket')
    events = models.ManyToManyField(LandmarkEvent,related_name='events',through='TourPackageLandmarkEvent')
    tourism_categories = models.ManyToManyField(TourismCategory,related_name='tourism_categories',through='TourPackageTourismCategory')
    package_maximium_budget = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    days = models.IntegerField(null=True)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
    
    def calculate_total_price(self):
        # total_cost = 0
        # if self.events is None:
        #     return None

        # arabic_countries = ['AE', 'BH', 'DJ', 'DZ', 'EG', 'IQ', 'JO', 'KW', 'LB', 'LY', 'MA', 'MR', 'OM', 'PS', 'QA', 'SA', 'SD', 'SO', 'SY', 'TN', 'YE']
        # today = timezone.now()
        # if self.user_created_by.nationality == 'EG':
        #     if self.user_created_by.birth_date:
        #         if (today-self.user_created_by.birth_date).days >= 21:
        #             ticket_class_name = 'Egyptian'
        #         else:
        #             ticket_class_name ='Student'
        #     else:
        #         ticket_class_name ='Egyptian'

        # elif self.user_created_by.nationality in arabic_countries:
        #     if self.user_created_by.birth_date:
        #         if (today-self.user_created_by.birth_date).days >= 21:
        #             ticket_class_name = 'Arab'
        #         else:
        #             ticket_class_name ='Student'
        #     else:
        #         ticket_class_name ='Arab'
            
        # else:
        #     if (today-self.user_created_by.birth_date).days >= 21:
        #         ticket_class_name = 'Foreigner'
        #     else:
        #         ticket_class_name ='Foreigner_Student'
        if self.tickets is None:
            return None
       
        tickets = Ticket.objects.filter(id__in=self.tickets).values('price')
        budget = tickets.aggregate(Sum('price'))['price__sum']
        if budget is None:
            budget = 0
        return budget
    
    def calculate_duration(self):
        if not self.start_date or not self.end_date:
            return None
        time_delta = self.end_date - self.start_date
        duration_in_days = time_delta.days
        # self.days = duration_in_days
        # self.save()
        return duration_in_days
                
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if not self.package_maximium_budget and hasattr(self, 'events'):
        #     self.package_maximium_budget = self.calculate_total_price()
        if not self.days and hasattr(self, 'start_date') and hasattr(self, 'end_date'):
            self.days = self.calculate_duration()

            
    def __str__(self):

        return f'{self.title}'

class TourPackageTourismCategory(models.Model):
    tourism_category = models.ForeignKey(TourismCategory,on_delete=models.CASCADE)
    tourpackage = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.tourpackage.title} => {self.tourism_category.name}'
    
class TourPackageTicket(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    tourpackage = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.tourpackage.title} => {self.ticket}'
    
class TourPackageLandmarkEvent(models.Model):
    event = models.ForeignKey(LandmarkEvent,on_delete=models.CASCADE)
    tourpackage = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.tourpackage.title} => {self.event}'

# # class UserTourPackage(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     tourpackage = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
#     created = models.DateTimeField(default=timezone.now, verbose_name="Creation Date")
#     active = models.BooleanField(default=True)