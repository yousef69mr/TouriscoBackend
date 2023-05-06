from django.contrib import admin
from .models import TourismCategory,TourismCategoryLanguageBased
# Register your models here.

class TourismCategoryAdmin(admin.ModelAdmin):
    
    model = TourismCategory
    ordering = ['id']
    list_display = ['id', 'name', 'image', 'created', 'active']
    list_display_links = ['id', 'name', 'image', 'created', 'active']
    list_filter = ['created', 'active']
    # list_editable =['description']


admin.site.register(TourismCategory,TourismCategoryAdmin)


class TourismCategoryLanguageBasedAdmin(admin.ModelAdmin):
    
    model = TourismCategoryLanguageBased
    ordering = ['id']
    list_display = ['id', 'title', 'categoryObject','lang', 'created', 'active']
    list_display_links = ['id', 'title', 'categoryObject','lang', 'created', 'active']
    list_filter = ['created','lang','categoryObject', 'active']
    # list_editable =['description']


admin.site.register(TourismCategoryLanguageBased,TourismCategoryLanguageBasedAdmin)