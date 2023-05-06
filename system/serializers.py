from rest_framework import serializers
from .models import (
    Language
)
# from TouriscoBackend.utils import translate_django_model


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'




