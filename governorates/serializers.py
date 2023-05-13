from rest_framework import serializers
from .models import Governorate,GovernorateLanguageBased
from system.serializers import LanguageSerializer

# default model
class GovernorateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Governorate
        fields = '__all__'


# language based model
class GovernoratesSerializer(serializers.ModelSerializer):
    governorate = GovernorateSerializer(source='govObject')
    language = LanguageSerializer(source='lang')

    class Meta:
        model = GovernorateLanguageBased
        fields = ('id', 'governorate', 'language','lang','govObject',
                  'title', 'governor', 'description', 'active', 'created')
        # lookup_field = 'lang_code'
        extra_kwargs = {
            # 'url': {'lookup_field': 'lang_code'}
            'govObject': {'write_only': True},
            'lang': {'write_only': True}
        }
