from rest_framework import serializers
# from django.utils import timezone
from .models import Landmark,LandmarkLanguageBased,LandmarkImage,LandmarkReview

from governorates.serializers import GovernorateSerializer
from system.serializers import LanguageSerializer
from TouriscoBackend.utils import translate_django_model


class LandmarkSerializer(serializers.ModelSerializer):
    governorate = GovernorateSerializer(source='govObject', read_only=True)

    class Meta:
        model = Landmark
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
                # 'url': {'lookup_field': 'lang_code'}
                'govObject': {'write_only': True},
                'typeCategoryObject': {'write_only': True}
            }
        
    def create(self, validated_data):
        # print(validated_data,"\n\n\n\n")
        governorate = validated_data.pop('govObject', None)
        # user = validated_data.pop()
        instance = Landmark.objects.create(govObject=governorate, **validated_data)
        user = validated_data.pop('user_created_by',None)
        
        if user.is_superuser:
            instance.active = True
        instance.save()
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
    category_type = serializers.CharField(source='category_type.title', read_only=True)
    # date_field = CustomDateField(source='created')

    class Meta:
        model = LandmarkLanguageBased
        fields = '__all__'
        # lookup_field = 'lang_code'
        read_only_fields = ['id','active']
        extra_kwargs = {
            # 'url': {'lookup_field': 'lang_code'}
            'landmarkObject': {'write_only': True},
            'lang': {'write_only': True}
        }

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
    
    # def to_representation(self, instance):
    #     return{
    #         'id': instance.id,
    #         'landmark': LandmarkSerializer(instance.landmarkObject).data,
    #         'language': LanguageSerializer(instance.lang).data,

    #     }

class LandmarkImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandmarkImage
        fields = '__all__'
        read_only_fields = ['id','active']
        

class LandmarkReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandmarkReview
        fields = '__all__'
        read_only_fields = ['id','active']