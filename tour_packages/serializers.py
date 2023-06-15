from rest_framework import serializers
from landmark_events.serializers import EventSerializer
from .models import TourPackage
from system.serializers import LanguageSerializer


class TourPackageSerializer(serializers.ModelSerializer):
    # event = EventSerializer(source='eventObject',read_only=True)

    class Meta:
        model = TourPackage
        fields = '__all__'
        read_only_fields = ['id','active']
        # extra_kwargs = {
        #     # 'url': {'lookup_field': 'lang_code'}
        #     'eventObject': {'write_only': True},
        # }


