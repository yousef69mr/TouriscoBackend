from rest_framework import serializers
from django.utils import timezone
from .models import Landmark,LandmarkLanguageBased
from governorates.serializers import GovernorateSerializer
from system.serializers import LanguageSerializer
from TouriscoBackend.utils import translate_django_model



class CustomDateField(serializers.ReadOnlyField):
    """
    Custom read-only field to handle timezone issues explicitly.
    """
    def to_representation(self, value):
        """
        Convert the datetime object to a date object and
        handle timezone issues in a different way.
        """
        if value is None:
            return None
        if isinstance(value, str):
            value = timezone.datetime.fromisoformat(value)

        # Convert the datetime object to a date object.
        date_obj = value.date()

        # Handle timezone issues in a different way.
        if self.context.get('request') is not None:
            tz = timezone.get_current_timezone()
            if value.tzinfo is not None:
                date_obj = value.astimezone(tz).date()
            else:
                date_obj = timezone.make_aware(value, tz).date()

        return date_obj


class LandmarkSerializer(serializers.ModelSerializer):
    governorate = GovernorateSerializer(source='govObject', read_only=True)

    class Meta:
        model = Landmark
        fields = '__all__'

        extra_kwargs = {
                # 'url': {'lookup_field': 'lang_code'}
                'govObject': {'write_only': True}
            }
    def create(self, validated_data):
        # print(validated_data,"\n\n\n\n")
        governorate = validated_data.pop('govObject', None)
        instance = Landmark.objects.create(
            govObject=governorate, **validated_data)

        return instance
    
    # def to_representation(self, instance):
    #     return {
    #         'name': instance.name,
    #         'area': instance.area,
    #         'governorate': GovernorateSerializer(instance.govObject).data
    #     }
    

class LandmarksSerializer(serializers.ModelSerializer):
    landmark = LandmarkSerializer(source='landmarkObject', read_only=True)
    language = LanguageSerializer(source='lang', read_only=True)
    # date_field = CustomDateField(source='created')

    class Meta:
        model = LandmarkLanguageBased
        fields = '__all__'
        # lookup_field = 'lang_code'
        extra_kwargs = {
            # 'url': {'lookup_field': 'lang_code'}
            'landmarkObject': {'write_only': True},
            'lang': {'write_only': True}
        }

    def create(self, validated_data):
        print(validated_data)
        landmark = validated_data.pop('landmarkObject', None)
        language = validated_data.pop('lang', None)

        instance = LandmarkLanguageBased.objects.create(
            landmarkObject=landmark, lang=language, **validated_data)
        # print(instance)
        translatedInstance = translate_django_model(
            instance, instance.lang.code.lower())

        print(translatedInstance)
        translatedInstance.save()
        return translatedInstance
    
    # def to_representation(self, instance):
    #     return{
    #         'id': instance.id,
    #         'landmark': LandmarkSerializer(instance.landmarkObject).data,
    #         'language': LanguageSerializer(instance.lang).data,

    #     }
