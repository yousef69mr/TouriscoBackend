from django.contrib import admin
from .models import LandmarkEvent,LandmarkEventLanguageBased
# Register your models here.


class EventAdmin(admin.ModelAdmin):
    model = LandmarkEvent
    ordering = ['id']
    list_display = ['id', 'name', 'landmarkObject',
                    'isMain', 'created', 'active']
    list_display_links = ['id', 'name', 'landmarkObject', 'created']
    list_filter = ['isMain','is_eternel', 'created', 'active']


admin.site.register(LandmarkEvent, EventAdmin)


class LandmarkEventLanguageBasedAdmin(admin.ModelAdmin):
    model = LandmarkEventLanguageBased
    ordering = ['id']
    list_display = ['id', 'title', 'lang', 'created', 'active']
    list_display_links = ['id', 'title', 'lang', 'created']
    list_filter = ['created', 'lang', 'active']


admin.site.register(LandmarkEventLanguageBased,
                    LandmarkEventLanguageBasedAdmin)
