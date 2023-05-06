from rest_framework import serializers
from .models import LandmarkEvent,LandmarkEventLanguageBased
from system.serializers import LanguageSerializer
from TouriscoBackend.utils import translate_django_model

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

