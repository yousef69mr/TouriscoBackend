
from rest_framework import serializers
from landmarks.serializers import LandmarkSerializer
from .models import TourismCategoryLanguageBased,TourismCategory
from system.serializers import LanguageSerializer
from TouriscoBackend.utils import translate_django_model


class TourismCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TourismCategory
        fields = '__all__'


class TourismCategoriesSerializer(serializers.ModelSerializer):
    category = TourismCategorySerializer(source='categoryObject',read_only=True)
    language = LanguageSerializer(source='lang',read_only=True)

    class Meta:
        model = TourismCategoryLanguageBased
        fields = ('id', 'category','categoryObject','lang','description', 'language', 'title', 'created','active')

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
