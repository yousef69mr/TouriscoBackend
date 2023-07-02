from django.contrib import admin
from .models import TourPackage,TourPackageTourismCategory,TourPackageTicket,TourPackageLandmarkEvent
# Register your models here.

class TourPackageAdmin(admin.ModelAdmin):
    model = TourPackage
    ordering = ['id']
    list_display = ['id', 'title', 'user_created_by','package_maximium_budget', 'created', 'active']
    list_display_links = ['id', 'title', 'package_maximium_budget', 'created']
    list_filter = ['created', 'active']
    search_fields = ['title','user_created_by']


admin.site.register(TourPackage, TourPackageAdmin)

class TourPackageTourismCategoryAdmin(admin.ModelAdmin):
    model = TourPackageTourismCategory
    ordering = ['id']
    list_display = ['id', 'tourpackage','tourism_category', 'created', 'active']
    list_display_links = ['id', 'tourpackage', 'tourism_category', 'created']
    list_filter = ['created', 'active']
    search_fields = ['tourpackage__title','user_created_by']


admin.site.register(TourPackageTourismCategory, TourPackageTourismCategoryAdmin)


class TourPackageTicketAdmin(admin.ModelAdmin):
    model = TourPackageTicket
    ordering = ['id']
    list_display = ['id', 'tourpackage','ticket', 'created', 'active']
    list_display_links = ['id', 'tourpackage', 'ticket', 'created']
    list_filter = ['created', 'active']
    search_fields = ['tourpackage__title','user_created_by']


admin.site.register(TourPackageTicket, TourPackageTicketAdmin)


class TourPackageLandmarkEventAdmin(admin.ModelAdmin):
    model = TourPackageLandmarkEvent
    ordering = ['id']
    list_display = ['id', 'tourpackage','event', 'created', 'active']
    list_display_links = ['id', 'tourpackage', 'event', 'created']
    list_filter = ['created', 'active']
    search_fields = ['tourpackage__title','user_created_by']


admin.site.register(TourPackageLandmarkEvent, TourPackageLandmarkEventAdmin)