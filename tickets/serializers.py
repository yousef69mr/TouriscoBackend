from rest_framework import serializers
from landmark_events.serializers import EventSerializer
from .models import Ticket,TicketLanguageBased
from system.serializers import LanguageSerializer
from TouriscoBackend.utils import translate_django_model


class TicketSerializer(serializers.ModelSerializer):
    event = EventSerializer(source='eventObject',read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
        extra_kwargs = {
            # 'url': {'lookup_field': 'lang_code'}
            'eventObject': {'write_only': True},
        }



class TicketsSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(source='ticketObject',read_only=True)
    language = LanguageSerializer(source='lang',read_only=True)

    class Meta:
        model = TicketLanguageBased
        fields = '__all__'

        extra_kwargs = {
            # 'url': {'lookup_field': 'lang_code'}
            'ticketObject': {'write_only': True},
            'lang': {'write_only': True}
        }
    
    def create(self, validated_data):
        # print(validated_data)
        ticket = validated_data.pop('ticketObject', None)
        language = validated_data.pop('lang', None)

        instance = TicketLanguageBased.objects.create(
            ticketObject=ticket, lang=language, **validated_data)
        # print(instance)
        translatedInstance = translate_django_model(
            instance, instance.lang.code.lower())

        # print(translatedInstance)
        translatedInstance.save()
        return translatedInstance