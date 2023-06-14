from django.contrib import admin
from .models import (
    TourismCategory,
    TourismCategoryLanguageBased,
    TypeCategory,
    TypeCategoryLanguageBased,
    TicketClassCategory,
    TicketClassCategoryLanguageBased
)
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

class TypeCategoryAdmin(admin.ModelAdmin):
    
    model = TypeCategory
    ordering = ['id']
    list_display = ['id', 'name', 'created', 'active']
    list_display_links = ['id', 'name', 'created', 'active']
    list_filter = ['created', 'active']
    # list_editable =['description']


admin.site.register(TypeCategory,TypeCategoryAdmin)


class TypeCategoryLanguageBasedAdmin(admin.ModelAdmin):
    
    model = TypeCategoryLanguageBased
    ordering = ['id']
    list_display = ['id', 'title', 'categoryObject','lang', 'created', 'active']
    list_display_links = ['id', 'title', 'categoryObject','lang', 'created', 'active']
    list_filter = ['created','lang','categoryObject', 'active']
    # list_editable =['description']


admin.site.register(TypeCategoryLanguageBased,TypeCategoryLanguageBasedAdmin)



class TicketClassCategoryAdmin(admin.ModelAdmin):
    
    model = TicketClassCategory
    ordering = ['id']
    list_display = ['id', 'name', 'created', 'active']
    list_display_links = ['id', 'name', 'created', 'active']
    list_filter = ['created', 'active']
    # list_editable =['description']


admin.site.register(TicketClassCategory,TicketClassCategoryAdmin)


class TicketClassCategoryLanguageBasedAdmin(admin.ModelAdmin):
    
    model = TicketClassCategoryLanguageBased
    ordering = ['id']
    list_display = ['id', 'title', 'categoryObject','lang', 'created', 'active']
    list_display_links = ['id', 'title', 'categoryObject','lang', 'created', 'active']
    list_filter = ['created','lang','categoryObject', 'active']
    # list_editable =['description']


admin.site.register(TicketClassCategoryLanguageBased,TicketClassCategoryLanguageBasedAdmin)