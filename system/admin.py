from django.contrib import admin

from .models import (
    Language,
    Governorate,
    GovernorateLanguageBased,
    Landmark,
    LandmarkLanguageBased,
    Ticket,
    TicketLanguageBased,
    LandmarkEvent,
    LandmarkEventLanguageBased
)


class LanguageAdmin(admin.ModelAdmin):
    model = Language
    ordering = ['id']
    list_display = ['id', 'name', 'code',
                    'country_code', 'dir', 'created', 'active']

    list_display_links = ['id', 'name', 'code', 'country_code']
    list_filter = ['created', 'active']


admin.site.register(Language, LanguageAdmin)


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


class EventAdmin(admin.ModelAdmin):
    model = LandmarkEvent
    ordering = ['id']
    list_display = ['id', 'name', 'landmarkObject',
                    'isMain', 'created', 'active']
    list_display_links = ['id', 'name', 'landmarkObject', 'created']
    list_filter = ['isMain', 'created', 'active']


admin.site.register(LandmarkEvent, EventAdmin)


class LandmarkEventLanguageBasedAdmin(admin.ModelAdmin):
    model = LandmarkEventLanguageBased
    ordering = ['id']
    list_display = ['id', 'title', 'lang', 'created', 'active']
    list_display_links = ['id', 'title', 'lang', 'created']
    list_filter = ['created', 'lang', 'active']


admin.site.register(LandmarkEventLanguageBased,
                    LandmarkEventLanguageBasedAdmin)


class TicketAdmin(admin.ModelAdmin):
    model = Ticket
    ordering = ['id']
    list_display = ['id', 'name', 'price', 'place', 'created', 'active']
    list_display_links = ['id', 'name', 'price', 'created']
    list_filter = ['price', 'created', 'active']


admin.site.register(Ticket, TicketAdmin)


class TicketLanguageBasedAdmin(admin.ModelAdmin):
    model = TicketLanguageBased
    ordering = ['id']
    list_display = ['id', 'title', 'lang', 'category', 'created', 'active']
    list_display_links = ['id', 'title', 'lang', 'created']
    list_filter = ['created', 'lang', 'category', 'active']


admin.site.register(TicketLanguageBased, TicketLanguageBasedAdmin)
