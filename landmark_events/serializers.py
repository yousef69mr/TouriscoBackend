from rest_framework import serializers
from .models import LandmarkEvent,LandmarkEventLanguageBased
from system.serializers import LanguageSerializer
from TouriscoBackend.utils import translate_django_model
from landmarks.serializers import LandmarkSerializer
import datetime
from django.utils import timezone

# main model

class EventSerializer(serializers.ModelSerializer):
    landmark = LandmarkSerializer(source='landmarkObject',read_only=True)

    class Meta:
        model = LandmarkEvent
        
        fields = '__all__'
        read_only_fields = ['id','active']

        extra_kwargs = {
            # 'url': {'lookup_field': 'lang_code'}
            'landmarkObject': {'write_only': True},
        }

    def create(self, validated_data):
        print(validated_data,"\n\n\n\n")
        landmark = validated_data.pop('landmarkObject', None)
        is_eternel = validated_data.pop('is_eternel', True)
        start_date = validated_data.pop('start_date', None)
        end_date = validated_data.pop('end_date', None)
        # print(is_eternel)
        if is_eternel:
            instance = LandmarkEvent.objects.create(landmarkObject=landmark,is_eternel=is_eternel,**validated_data)
        else:
            instance = LandmarkEvent.objects.create(landmarkObject=landmark,start_date=start_date,end_date=end_date,is_eternel=is_eternel, **validated_data)
        # print(instance.start_date,instance.end_date)
        return instance

# language based model
class EventsSerializer(serializers.ModelSerializer):

    language = LanguageSerializer(source='lang', read_only=True)
    event = EventSerializer(source='eventObject', read_only=True)

    class Meta:
        model = LandmarkEventLanguageBased

        fields = '__all__'
        read_only_fields = ['id','active']
        
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

