
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)


from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import (
    
    TicketsSerializer,
)
from .models import (
    Language,  
    TicketLanguageBased
   
)

# Create your views here.

class TicketsView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = 'lang_code'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        if language is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        tickets = TicketLanguageBased.objects.filter(lang=language)
        # print(governorates)
        serializer = TicketsSerializer(tickets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        mainserializer = TicketsSerializer(data=request.data)
        if mainserializer.is_valid():
            mainserializer.save()

            return Response(mainserializer.data, status=status.HTTP_201_CREATED)
        return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)
