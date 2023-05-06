from rest_framework import serializers
from landmarks.serializers import LandmarkSerializer
from .models import Ticket,TicketLanguageBased
from system.serializers import LanguageSerializer


class TicketSerializer(serializers.ModelSerializer):
    landmark = LandmarkSerializer(source='place')

    class Meta:
        model = Ticket
        fields = ('id', 'price', 'landmark', 'created', 'active')


class TicketsSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(source='ticketObject')
    language = LanguageSerializer(source='lang')

    class Meta:
        model = TicketLanguageBased
        fields = ('id', 'ticket', 'language', 'title', 'category')
