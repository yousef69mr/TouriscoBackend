from rest_framework import serializers
from users.serializers import UserSerializer
from nudenet import NudeDetector
from .models import (
    Language,
    Image
)
# from TouriscoBackend.utils import translate_django_model


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
        read_only_fields = ['id','active']


class ImageSerializer(serializers.ModelSerializer):
    # user = UserSerializer(source='userObject',read_only=True)
    class Meta:
        model = Image
        fields = '__all__'
        read_only_fields = ['id','active']
        # read_only_fields = ['id']
        
    def create(self, validated_data):
        print(validated_data)
        image = validated_data.pop('image')
        user= validated_data.pop('userObject')
        print(type(user))
        
        # detector = NudeDetector()
        # contains_nudity = detector.detect(image.image.path)
        # print(contains_nudity)
        instance = Image.objects.create(userObject=user,image=image,**validated_data)
        print(instance)
        return instance
    

