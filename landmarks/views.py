
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)


from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import (
    LandmarkSerializer,
    LandmarksSerializer,
   
)
from .models import (
    Language,
    Landmark,
    LandmarkLanguageBased,
)

# Create your views here.



class LandmarkListView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = 'lang_code'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)

        landmarks = LandmarkLanguageBased.objects.all().filter(lang=language)
        # print(governorates)
        serializer = LandmarksSerializer(landmarks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LandmarkInSpecificGovernorate(APIView):
    lookup_field = ['lang_code', 'landmark_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, governorate_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        # governorate = get_object_or_404(Governorate, id=governorate_id)
        # print(governorate)
        langlandmarks = LandmarkLanguageBased.objects.filter(landmarkObject__govObject__id=governorate_id, lang=language)
        print(langlandmarks)
        serializer = LandmarksSerializer(langlandmarks,many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LandmarkView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = ['lang_code', 'landmark_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, landmark_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        landmark = get_object_or_404(Landmark, id=landmark_id)
        print(landmark)
        langlandmark = get_object_or_404(
            LandmarkLanguageBased, landmarkObject=landmark, lang=language)
        print(langlandmark)
        serializer = LandmarksSerializer(langlandmark)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LandmarkCoreListView(APIView):
    def get(self, request, format=None):

        landmarks = Landmark.objects.all()
        # print(governorates)
        serializer = LandmarkSerializer(landmarks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        mainserializer = LandmarkSerializer(data=request.data)

        if mainserializer.is_valid():
            mainserializer.save()

            landmark = get_object_or_404(
                Landmark, id=mainserializer.data.get("id"))

            # print(event, "\n\n\n")
            languages = Language.objects.all()

            request.data['landmarkObject'] = landmark.id

            landmarklangVersions = []
            landmarklangVersionsErrors = []
            for language in languages:
                request.data['lang'] = language.id
                # print(request.data, "\n\n")
                serializer = LandmarksSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    landmarklangVersions.append(serializer.data)
                else:
                    landmarklangVersionsErrors.append(serializer.errors)

            if len(landmarklangVersionsErrors) > 0:
                return Response(landmarklangVersionsErrors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(landmarklangVersions, status=status.HTTP_201_CREATED)

        return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)

