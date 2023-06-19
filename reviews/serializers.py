from rest_framework import serializers
from .models import ReviewImage,Review
from system.serializers import ImageSerializer
from users.serializers import UserReviewSerializer


class ReviewImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model= ReviewImage
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = UserReviewSerializer(source='userObject',read_only=True)
    images = ImageSerializer(many=True,read_only=True)
    class Meta:
        model= Review
        fields = '__all__'
        read_only_fields = ['id','active']
        # extra_kwargs = {
        #     'content_type': {'write_only': True},
        # }
