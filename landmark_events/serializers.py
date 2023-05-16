from rest_framework import serializers
from .models import LandmarkEvent,LandmarkEventLanguageBased
from system.serializers import LanguageSerializer
from TouriscoBackend.utils import translate_django_model
from landmarks.serializers import LandmarkSerializer

# main model


class EventSerializer(serializers.ModelSerializer):
    landmark = LandmarkSerializer(source='landmarkObject',read_only=True)
    class Meta:
        model = LandmarkEvent
        # fields = ('id','name','','landmarkObject','isMain','created','active')
        fields = '__all__'

        extra_kwargs = {
            # 'url': {'lookup_field': 'lang_code'}
            'landmarkObject': {'write_only': True},
        }

    # def create(self, validated_data):
    #     # print(validated_data,"\n\n\n\n")
    #     landmark = validated_data.pop('landmarkObject', None)
    #     instance = LandmarkEvent.objects.create(
    #         landmarkObject=landmark, **validated_data)

    #     return instance

# language based model
class EventsSerializer(serializers.ModelSerializer):

    language = LanguageSerializer(source='lang', read_only=True)
    event = EventSerializer(source='eventObject', read_only=True)

    class Meta:
        model = LandmarkEventLanguageBased

        fields = '__all__'
        
        extra_kwargs = {
            # 'url': {'lookup_field': 'lang_code'}
            'eventObject': {'write_only': True},
            'lang': {'write_only': True}
        }

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

