
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)


from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import (
    GovernoratesSerializer,
    GovernorateSerializer,
)
from .models import (
    Governorate,
    GovernorateLanguageBased,
)
from system.models import Language

# Create your views here.

class GovernorateListView(APIView):
    # queryset = GovernorateLanguageBased.objects.all()
    # serializer_class = GovernoratesSerializer
    lookup_field = 'lang_code'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)

        governorates = GovernorateLanguageBased.objects.filter(lang=language).order_by('-govObject__population')
        # print(governorates)
        serializer = GovernoratesSerializer(governorates, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = GovernoratesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GovernorateCoreListView(APIView):
    def get(self, request, format=None):

        governorates = get_list_or_404(Governorate)
        # print(governorates)
        serializer = GovernorateSerializer(governorates, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GovernorateView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = ['lang_code', 'landmark_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, governorate_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        governorate = get_object_or_404(Governorate, id=governorate_id)
        langGovernorate = get_object_or_404(GovernorateLanguageBased, govObject=governorate, lang=language)
        print(langGovernorate)
        serializer = GovernoratesSerializer(langGovernorate)

        return Response(serializer.data, status=status.HTTP_200_OK)

