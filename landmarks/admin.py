from django.contrib import admin
from .models import Landmark,LandmarkLanguageBased
# Register your models here.


class LandmarkAdmin(admin.ModelAdmin):
    model = Landmark
    ordering = ['id']
    list_display = ['id', 'name', 'height',
                    'govObject', 'area', 'created', 'active']
    list_display_links = ['id', 'name', 'area', 'created']
    list_filter = ['created', 'active']


admin.site.register(Landmark, LandmarkAdmin)


class LandmarkLanguageBasedAdmin(admin.ModelAdmin):
    model = LandmarkLanguageBased
    ordering = ['id']
    list_display = ['id', 'title', 'lang', 'created', 'active']
    list_display_links = ['id', 'title', 'lang', 'created']
    list_filter = ['created', 'lang', 'active']


admin.site.register(LandmarkLanguageBased, LandmarkLanguageBasedAdmin)

