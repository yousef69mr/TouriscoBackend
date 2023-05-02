from rest_framework import serializers
from .models import (
    Language,
    GovernorateLanguageBased,
    Governorate,
    Landmark,
    LandmarkLanguageBased,
    TicketLanguageBased,
    Ticket,
    LandmarkEvent,
    LandmarkEventLanguageBased
)
from backend.utils import translate_django_model


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


# default model
class GovernorateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Governorate
        fields = '__all__'


# language based model
class GovernoratesSerializer(serializers.ModelSerializer):
    governorate = GovernorateSerializer(source='govObject')
    language = LanguageSerializer(source='lang')

    class Meta:
        model = GovernorateLanguageBased
        fields = ('id', 'governorate', 'language',
                  'title', 'governor', 'description', 'active', 'created')
        # lookup_field = 'lang_code'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'lang_code'}
        # }


class LandmarkSerializer(serializers.ModelSerializer):
    governorate = GovernorateSerializer(source='govObject', read_only=True)

    class Meta:
        model = Landmark
        fields = '__all__'

    def create(self, validated_data):
        # print(validated_data,"\n\n\n\n")
        governorate = validated_data.pop('govObject', None)
        instance = Landmark.objects.create(
            govObject=governorate, **validated_data)

        return instance


class LandmarksSerializer(serializers.ModelSerializer):
    landmark = LandmarkSerializer(source='landmarkObject', read_only=True)
    language = LanguageSerializer(source='lang', read_only=True)

    class Meta:
        model = LandmarkLanguageBased
        fields = ('id',  'title', 'founder', 'landmarkObject', 'landmark',
                  'lang', 'language', 'address', 'description')
        # lookup_field = 'lang_code'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'lang_code'}
        # }

    def create(self, validated_data):
        # print(validated_data)
        landmark = validated_data.pop('landmarkObject', None)
        language = validated_data.pop('lang', None)

        instance = LandmarkLanguageBased.objects.create(
            landmarkObject=landmark, lang=language, **validated_data)
        # print(instance)
        translatedInstance = translate_django_model(
            instance, instance.lang.code.lower())

        # print(translatedInstance)
        translatedInstance.save()
        return translatedInstance

# main model


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandmarkEvent
        fields = '__all__'


# language based model
class EventsSerializer(serializers.ModelSerializer):

    language = LanguageSerializer(source='lang', read_only=True)
    event = EventSerializer(source='eventObject', read_only=True)

    class Meta:
        model = LandmarkEventLanguageBased

        fields = ('id', 'eventObject', 'lang', 'event',
                  'language', 'title', 'active')

    def create(self, validated_data):
        # print(validated_data)
        event = validated_data.pop('eventObject', None)
        language = validated_data.pop('lang', None)

        instance = LandmarkEventLanguageBased.objects.create(
            eventObject=event, lang=language, **validated_data)
        # print(instance)
        translatedInstance = translate_django_model(
            instance, instance.lang.code.lower())

        # print(translatedInstance)
        translatedInstance.save()
        return translatedInstance


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
