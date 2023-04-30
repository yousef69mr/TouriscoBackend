from rest_framework import serializers
# from system.models import Language, GovernorateLanguageBased, Governorate, Landmark, LandmarkLanguageBased, TicketLanguageBased, Ticket


# class LanguageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Language
#         fields = '__all__'


# class GovernorateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Governorate
#         fields = '__all__'


# class GovernoratesSerializer(serializers.ModelSerializer):
#     governorate = GovernorateSerializer(source='gov')
#     language = LanguageSerializer(source='lang')

#     class Meta:
#         model = GovernorateLanguageBased
#         fields = ('id', 'governorate', 'language',
#                   'title', 'governor', 'description', 'active', 'created')
#         # lookup_field = 'lang_code'
#         # extra_kwargs = {
#         #     'url': {'lookup_field': 'lang_code'}
#         # }


# class LandmarkSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Landmark
#         fields = '__all__'


# class LandmarksSerializer(serializers.ModelSerializer):
#     landmark = LandmarkSerializer(source='place')
#     language = LanguageSerializer(source='lang')

#     class Meta:
#         model = LandmarkLanguageBased
#         fields = ('id', 'landmark', 'language', 'name', 'founder')
#         # lookup_field = 'lang_code'
#         # extra_kwargs = {
#         #     'url': {'lookup_field': 'lang_code'}
#         # }


# class TicketSerializer(serializers.ModelSerializer):
#     landmark = LandmarkSerializer(source='place')

#     class Meta:
#         model = Ticket
#         fields = ('id', 'price', 'landmark', 'created', 'active')


# class TicketsSerializer(serializers.ModelSerializer):
#     ticket = TicketSerializer(source='ticketObject')
#     language = LanguageSerializer(source='lang')

#     class Meta:
#         model = TicketLanguageBased
#         fields = ('id', 'ticket', 'language', 'title', 'category')
