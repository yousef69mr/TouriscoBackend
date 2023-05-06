from django.contrib import admin
from .models import Governorate,GovernorateLanguageBased
# Register your models here.

class GovernorateAdmin(admin.ModelAdmin):
    model = Governorate
    ordering = ['id']
    list_display = ['id', 'name', 'area', 'population', 'created', 'active']
    list_display_links = ['id', 'name', 'population', 'area', 'created']
    list_filter = ['created', 'active']
    # list_editable =['population']


admin.site.register(Governorate, GovernorateAdmin)


class GovernorateLanguageBasedAdmin(admin.ModelAdmin):
    model = GovernorateLanguageBased
    ordering = ['id']
    list_display = ['id', 'title', 'lang', 'created', 'active']
    list_display_links = ['id', 'title', 'lang', 'created']
    list_filter = ['created', 'lang', 'active']
    # list_editable =['description']


admin.site.register(GovernorateLanguageBased, GovernorateLanguageBasedAdmin)