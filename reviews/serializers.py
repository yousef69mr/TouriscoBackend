from rest_framework import serializers
from .models import ReviewImage,Review


class ReviewImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model= ReviewImage
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model= Review
        fields = '__all__'
        read_only_fields = ['id','active']
        # extra_kwargs = {
        #     'content_type': {'write_only': True},
        # }
