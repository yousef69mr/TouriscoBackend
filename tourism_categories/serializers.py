
from rest_framework import serializers
from landmarks.serializers import LandmarkSerializer
from .models import TourismCategoryLanguageBased,TourismCategory,TypeCategory,TypeCategoryLanguageBased
from system.serializers import LanguageSerializer
from TouriscoBackend.utils import translate_django_model


class TourismCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TourismCategory
        fields = '__all__'
        read_only_fields = ['id','active']


class TourismCategoriesSerializer(serializers.ModelSerializer):
    category = TourismCategorySerializer(source='categoryObject',read_only=True)
    language = LanguageSerializer(source='lang',read_only=True)

    class Meta:
        model = TourismCategoryLanguageBased
        fields = '__all__'
        read_only_fields = ['id','active']

        extra_kwargs = {
            'categoryObject': {'write_only': True},
            'lang': {'write_only': True}
        }
    
    def create(self, validated_data):
        # print(validated_data)
        category = validated_data.pop('categoryObject', None)
        language = validated_data.pop('lang', None)

        instance = TourismCategoryLanguageBased.objects.create(
            categoryObject=category, lang=language, **validated_data)
        # print(instance)
        translatedInstance = translate_django_model(
            instance, instance.lang.code.lower())

        # print(translatedInstance)
        translatedInstance.save()
        return translatedInstance



class TypeCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeCategory
        fields = '__all__'
        read_only_fields = ['id','active']


class TypeCategoriesSerializer(serializers.ModelSerializer):
    category = TourismCategorySerializer(source='categoryObject',read_only=True)
    language = LanguageSerializer(source='lang',read_only=True)

    class Meta:
        model = TypeCategoryLanguageBased
        fields = '__all__'
        read_only_fields = ['id','active']

        extra_kwargs = {
            'categoryObject': {'write_only': True},
            'lang': {'write_only': True}
        }
    
    def create(self, validated_data):
        # print(validated_data)
        category = validated_data.pop('categoryObject', None)
        language = validated_data.pop('lang', None)

        instance = TypeCategoryLanguageBased.objects.create(categoryObject=category, lang=language, **validated_data)
        # print(instance)
        translatedInstance = translate_django_model(instance, instance.lang.code.lower())

        # print(translatedInstance)
        translatedInstance.save()
        return translatedInstance
