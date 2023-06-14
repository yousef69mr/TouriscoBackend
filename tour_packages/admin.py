from django.contrib import admin
from .models import TourPackage
# Register your models here.

class TourPackageAdmin(admin.ModelAdmin):
    model = TourPackage
    ordering = ['id']
    list_display = ['id', 'title', 'user_created_by','package_maximium_budget', 'created', 'active']
    list_display_links = ['id', 'title', 'package_maximium_budget', 'created']
    list_filter = ['created', 'active']
    search_fields = ['title','user_created_by']


admin.site.register(TourPackage, TourPackageAdmin)
