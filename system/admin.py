from django.contrib import admin

from .models import (
    Language,
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




