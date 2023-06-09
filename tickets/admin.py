from django.contrib import admin
from .models import Ticket,TicketLanguageBased
# Register your models here.


class TicketAdmin(admin.ModelAdmin):
    model = Ticket
    ordering = ['id']
    list_display = ['id', 'name', 'price', 'eventObject', 'created', 'active']
    list_display_links = ['id', 'name', 'price', 'created']
    list_filter = ['created', 'active']


admin.site.register(Ticket, TicketAdmin)


class TicketLanguageBasedAdmin(admin.ModelAdmin):
    model = TicketLanguageBased
    ordering = ['id']
    list_display = ['id', 'title', 'lang', 'ticket_class_category', 'created', 'active']
    list_display_links = ['id', 'title', 'lang', 'created']
    list_filter = ['created', 'lang', 'active']


admin.site.register(TicketLanguageBased, TicketLanguageBasedAdmin)
