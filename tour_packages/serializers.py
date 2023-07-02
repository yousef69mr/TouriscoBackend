from rest_framework import serializers
from landmark_events.serializers import EventSerializer
from .models import TourPackage,TourPackageTourismCategory,TourPackageLandmarkEvent,TourPackageTicket
from categories.serializers import TourismCategorySerializer
from tickets.serializers import TicketSerializer


class TourPackageSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True,read_only=True)
    tickets = TicketSerializer(many=True,read_only=True)
    tourism_categories = TourismCategorySerializer(many=True,read_only=True)
    
    class Meta:
        model = TourPackage
        fields = '__all__'
        read_only_fields = ['id','active']
        # extra_kwargs = {
        #     # 'url': {'lookup_field': 'lang_code'}
        #     'eventObject': {'write_only': True},
        # }


class TourPackageTourismCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TourPackageTourismCategory
        fields = '__all__'
        read_only_fields = ['id']


class TourPackageLandmarkEventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TourPackageLandmarkEvent
        fields = '__all__'
        read_only_fields = ['id']


class TourPackageTicketSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TourPackageTicket
        fields = '__all__'
        read_only_fields = ['id']

