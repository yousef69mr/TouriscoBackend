from django.contrib import admin

from .models import (
    Language,
    Image
#     Governorate,
#     GovernorateLanguageBased,
#     Landmark,
#     LandmarkLanguageBased,
#     Ticket,
#     TicketLanguageBased,
#     LandmarkEvent,
#     LandmarkEventLanguageBased
)


class LanguageAdmin(admin.ModelAdmin):
    model = Language
    ordering = ['id']
    list_display = ['id', 'name', 'code',
                    'country_code', 'dir', 'created', 'active']

    list_display_links = ['id', 'name', 'code', 'country_code']
    list_filter = ['created', 'active']


admin.site.register(Language, LanguageAdmin)


class ImageAdmin(admin.ModelAdmin):
    model = Image
    ordering = ['id']
    list_display = ['id','image', 'created', 'active']
    list_display_links = ['id' , 'created']
    list_filter = ['created', 'active']
admin.site.register(Image,ImageAdmin)
