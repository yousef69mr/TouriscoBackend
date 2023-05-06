from rest_framework import serializers
from .models import Landmark,LandmarkLanguageBased
from governorates.serializers import GovernorateSerializer
from system.serializers import LanguageSerializer
from TouriscoBackend.utils import translate_django_model


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
